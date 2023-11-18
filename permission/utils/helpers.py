from rest_framework.viewsets import ModelViewSet
from django.urls.resolvers import ResolverMatch
from typing import Union
from django.urls.resolvers import URLPattern
import importlib
import os
import re
import itertools


from django.conf import settings
from django.db import IntegrityError
from django.urls import URLPattern, URLResolver

from rest_framework.viewsets import ViewSet
from typing import Callable, Optional, List, Any, Union, Type, Dict, Set


from permission.models import Permission


HTTP_METHODS = ["get", "post", "put", "patch", "delete"]
REST_ACTIONS = [
    "create", "list", "update", "destroy",
    "partial_update", "retrieve"]


def remove_special_characters(string: str) -> str:
    """Removes special characters from a string.

    Args:
        string (str): The input string.

    Returns:
        str: The string with special characters removed.
    """
    return re.sub(r'[\n\t]', '', string).strip()


def get_detail(action: Callable[..., Optional[str]]) -> Optional[str]:
    """
    Get the docstring from the given action.

    Args:
        action: The action function.

    Returns:
        The docstring of the action function, or None if it is not available.
    """
    doc_string = action.__doc__ or ""
    return remove_special_characters(doc_string)


def intersects(list1: List, list2: List) -> bool:
    """
    Check if any element in list1 is present in list2.

    Args:
        list1 (List): The first list.
        list2 (List): The second list.

    Returns:
        bool: True if there is any element common to both lists, False otherwise.
    """
    return any(element in list2 for element in list1)


def is_django_function_view(url: URLPattern) -> bool:
    """
    Check if the given URL pattern corresponds to a Django function-based view.

    Args:
        url (URLPattern): The URL pattern to check.

    Returns:
        bool: True if the URL pattern corresponds to a function-based view, False otherwise.
    """
    return not getattr(url.callback, "cls", None) and not getattr(url.callback, "view_class", None)


def is_django_class_view(url: Any) -> bool:
    """Check if the given URL is a Django class-based view.

    Args:
        url (Any): The URL to check.

    Returns:
        bool: True if the URL is a Django class-based view, False otherwise.
    """
    cls: Optional[Callable] = getattr(url.callback, "cls", getattr(url.callback, "view_class", None))
    return cls is not None and not re.search("WrappedAPIView", str(url.callback)) and any(method in dir(cls) for method in HTTP_METHODS)


def is_rest_decorated_view(url: Union[URLPattern, URLResolver]) -> bool:
    """Check if the URL callback is decorated with @api_view

    Args:
        url (Union[URLPattern, URLResolver]): The URL pattern or resolver object

    Returns:
        bool: True if the URL callback is decorated with @api_view, else False
    """
    return "WrappedAPIView" in str(url.callback)


def is_rest_model_viewset(url: URLPattern) -> bool:
    """
    Check if the given URL pattern corresponds to a Django ModelViewSet.

    Args:
        url (URLPattern): The URL pattern to check.

    Returns:
        bool: True if the URL pattern corresponds to a ModelViewSet, False otherwise.
    """

    cls: Type[Any] = getattr(url.callback, "cls", None)
    return bool(
        set(REST_ACTIONS).intersection(dir(cls)) and cls.queryset.model
    )


def is_rest_non_model_viewset(url: ResolverMatch) -> bool:
    """
    Check if the given URL resolver match corresponds to a non-model viewset.

    Args:
        url (ResolverMatch): The URL resolver match object.

    Returns:
        bool: True if the URL corresponds to a non-model viewset, False otherwise.
    """
    try:
        callback_cls = url.callback.cls
        name_frags = url.name.split("-")[1:]
    except AttributeError:
        return False

    action = "_".join(name_frags)
    if set(["list", "create", "retrieve", "update", "partial_update", "destroy"]).intersection(dir(callback_cls)):
        return not hasattr(callback_cls, "queryset")
    return hasattr(callback_cls, action)


def get_django_function_view_action(url: URLPattern) -> callable:
    """
    Get the callback function from a Django URLPattern.

    Args:
        url (URLPattern): The URLPattern object.

    Returns:
        callable: The callback function.
    """
    return url.callback


def get_django_class_view_action(url: Any, method: str) -> Optional[Type]:
    """
    Retrieves the specified method from the Django class-based view.

    Args:
        url (Any): The URL pattern.
        method (str): The name of the method to retrieve.

    Returns:
        Optional[Type]: The method from the Django class-based view, or None if it does not exist.
    """
    cls: Optional[Type] = getattr(url.callback, "cls", None) or getattr(url.callback, "view_class")
    return getattr(cls, method, None)


def get_rest_decorated_view_action(url: Callable[..., None]) -> Callable[..., None]:
    """
    Returns the callback function from the given URL.

    Args:
        url (Callable[..., None]): The URL object.

    Returns:
        Callable[..., None]: The callback function.
    """
    return url.callback


def get_rest_model_viewset_action(url: URLPattern, action_name: str) -> Optional[callable]:
    """
    Retrieve the specified action method from the viewset class.

    Args:
        url (URLPattern): The URL pattern object.
        action_name (str): The name of the action method.

    Returns:
        callable: The specified action method, or None if it does not exist.
    """
    cls: ViewSet = url.callback.cls
    return getattr(cls, action_name, None)


def get_rest_non_model_viewset_action(url: Callable) -> Callable:
    """
    Returns the action method corresponding to the given URL.

    Args:
        url (Callable): The URL callback function.

    Returns:
        Callable: The action method corresponding to the URL.
    """
    cls = getattr(url.callback, "cls")
    frags = url.name.split("-")

    def get_action(frags: List[str]) -> Callable:
        """
        Retrieve the action based on the given fragments.

        Args:
            frags: A list of strings representing the action fragments.

        Returns:
            The action corresponding to the fragments.

        """
        action_name = "_".join(frags[1:])
        return getattr(cls, action_name, get_action(frags))

    return get_action(frags)


def get_django_function_view_permission(url: str) -> List[Dict[str, str]]:
    """
    Get the permission for a Django function-based view.

    Args:
        url (str): The URL of the view.

    Returns:
        List[Dict[str, str]]: A list containing a single dictionary with the permission details.
    """
    action: str = get_django_function_view_action(url)
    return [{"method": "any", "detail": get_detail(action)}]


def get_django_class_view_permission(url: str) -> List[Dict[str, Optional[str]]]:
    """
    Get permissions for each HTTP method in a Django class-based view.

    Args:
        url (str): The URL pattern for the view.

    Returns:
        List[Dict[str, Optional[str]]]: A list of dictionaries containing the method and detail
        for each HTTP method that has a corresponding action in the view. The detail is optional
        and may be None if no action is found for the method.
    """
    http_methods = ["get", "post", "put", "patch", "delete"]
    permissions = [
        {
            "method": method,
            "detail": get_detail(get_django_class_view_action(url, method))
        }
        for method in http_methods
        if get_django_class_view_action(url, method)
    ]
    return permissions


def get_rest_decorated_view_permission(url: URLPattern) -> List[Dict[str, str]]:
    """
    Get the permissions for a REST decorated view.

    Args:
        url (URLPattern): The URL pattern.

    Returns:
        List[Dict[str, str]]: The list of permissions.
    """
    permissions = [
        {
            "method": method,
            "detail": get_detail(get_rest_decorated_view_action(url))
        }
        for method in url.callback.cls.http_method_names
        if method != "options"
    ]
    return permissions


def get_rest_model_viewset_permission(url: Any) -> List[Dict[str, Any]]:
    """
    Get the permissions for a REST model viewset.

    Args:
        url (Any): The URL.

    Returns:
        List[Dict[str, Any]]: The list of permissions.
    """
    detail_action_map: Dict[str, str] = {
        "retrieve": "get",
        "destroy": "delete",
        "update": "put",
        "partial_update": "patch"
    }
    list_action_map: Dict[str, str] = {
        "list": "get",
        "create": "post"
    }
    permissions: List[Dict[str, Any]] = []

    if re.match(r".*?-detail", url.name):
        for action_name in detail_action_map:
            action = get_rest_model_viewset_action(url, action_name)
            if action:
                permissions.append({
                    "method": detail_action_map[action_name],
                    "detail": get_detail(action)
                })
    elif re.match(r".*?-list", url.name):
        for action_name in list_action_map:
            action = get_rest_model_viewset_action(url, action_name)
            if action:
                permissions.append({
                    "method": list_action_map[action_name],
                    "detail": get_detail(action)
                })
    else:
        return get_rest_non_model_viewset_permission(url)

    return permissions


def get_rest_non_model_viewset_permission(url: URLPattern) -> List[Dict[str, str]]:
    """
    Retrieves the permissions of a non-model viewset action.

    Args:
        url (URLPattern): The URL pattern of the viewset action.

    Returns:
        List[Dict[str, str]]: A list of permissions, where each permission is a dictionary with the keys 'method' and 'detail'.
    """
    action = get_rest_non_model_viewset_action(url)
    permissions = [
        {
            "method": method,
            "detail": remove_special_characters(action.__doc__ or "")
        }
        for method in list(action.bind_to_methods)
    ]
    return permissions


def get_permission(url: str) -> Dict[str, Callable[[str], str]]:
    """Returns a map of permission name and HTTP method.

    Args:
        url: The URL to check permissions for.

    Returns:
        A dictionary mapping permission names to functions that return the HTTP method.
    """

    permission_map: Dict[Callable[[str], bool], Callable[[str], str]] = {
        is_django_function_view: get_django_function_view_permission,
        is_rest_decorated_view: get_rest_decorated_view_permission,
        is_rest_model_viewset: get_rest_model_viewset_permission,
        is_rest_non_model_viewset: get_rest_model_viewset_permission,
        is_django_class_view: get_django_class_view_permission
    }

    for check_func, get_permission_func in permission_map.items():
        if check_func(url):
            return get_permission_func(url)


def normalize_url(url: str) -> str:
    """
    Normalizes the given URL by adding a leading slash and trailing slash if necessary.

    Args:
        url (str): The URL to normalize.

    Returns:
        str: The normalized URL.
    """
    t = url.strip("^$")  # remove leading and trailing ^ and $

    if not t.startswith("/"):
        t = "/" + t

    if not t.endswith("/"):
        t = t + "/"

    return t


def flatten(nested_permissions: List[List[Any]]) -> List[Any]:
    """
    Flatten a nested list of permissions.

    Args:
        nested_permissions: A nested list of permissions.

    Returns:
        A flat list of permissions.
    """
    return list(itertools.chain(*nested_permissions))


def get_urls_for(app_name: str) -> List[Dict[str, Any]]:
    """
    Get the URLs for the specified app.

    Args:
        app_name (str): The name of the app.

    Returns:
        List[str]: The URLs for the specified app.
    """
    try:
        module_name = f"{app_name}.urls"
        urlpatterns = importlib.import_module(module_name).urlpatterns
    except ImportError:
        return []
    urls = [get_url_meta(url) for url in urlpatterns if get_url_meta(url)]
    return urls


def get_url_meta(url: URLPattern) -> Dict[str, str]:
    """
    Returns the name, URL, and permissions for a given URL.

    Args:
        url (URLPattern): The URL pattern object.

    Returns:
        Dict[str, str]: A dictionary containing the name, URL, and permissions.
    """
    name: str = url.name
    url_pattern: str = normalize_url(url.pattern.regex.pattern)
    permissions: str = get_permission(url)

    return {
        "name": name,
        "url": url_pattern,
        "permissions": permissions
    }


def get_apps() -> Set[str]:
    """
    Get the set of installed apps that exist as directories in the current working directory.

    Returns:
        A set of app names that are both installed and exist as directories.
    """
    dirs = [dir for dir in os.listdir(os.getcwd()) if os.path.isdir(dir)]
    installed_apps = set(settings.INSTALLED_APPS)
    return set(dirs).intersection(installed_apps)


def get_urls(exclude=[], filtero=""):
    apps = get_apps()

    urls = [get_urls_for(app) for app in apps if app not in set(exclude)]

    return [aurl for url in urls for aurl in url if re.search(filtero, aurl['url'])]


def create_permissions() -> None:
    """
    Retrieves URLs and creates permissions for each URL.

    :return: None
    """
    permissions: List[Permission] = []
    existing_actions: set[str] = set()
    urls: List[dict] = get_urls()

    for url in urls:
        try:
            for permission in url['permissions']:
                pair = (url['name'], permission['method'])
                if pair in existing_actions:
                    continue
                existing_actions.add(pair)
                permissions.append(
                    Permission(
                        name=url['name'],
                        url=url['url'],
                        method=permission['method'],
                        description=permission['detail'],
                    )
                )
        except Exception as exp:
            print("=========================", url)
            print(str(exp))

    Permission.objects.all().delete()
    Permission.objects.bulk_create(permissions)
