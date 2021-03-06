"""
Module containing API request-to-response logic, independent of the
webserver or transit format. Main endpoint is `query`, which takes a
dictionary request and returns a dictionary response.
"""

import whales.models
import whales.util.chess


class APIError(Exception):
    """
    Exception that indicates user error while processing API request.
    """

    pass


def normal_response(response):
    """
    Construct non-error response for API from giving response
    dictionary. Return a dictionary.
    """
    response = dict(response)
    response["error"] = None
    return response


def error_response(message):
    """
    Construct error response for API containing given error message.
    Return a dictionary.
    """
    return {"error": message}


def query(request):
    """
    Given a dictionary with an API request, return a dictionary with the
    response.
    """
    if not isinstance(request, dict):
        return error_response("invalid JSON")
    if "command" not in request:
        return error_response("no command specified")
    command = request["command"]
    if command == "list_models":
        info = whales.models.get_model_info()
        return normal_response({"models": info})
    if command == "get_move":
        for param in ["model", "pgn"]:
            if param not in request:
                return error_response(
                    "missing required parameter {}".format(repr(param))
                )
        model_name = request["model"]
        old_pgn = request["pgn"]
        try:
            new_pgn = whales.models.run_model(model_name, old_pgn)
        except whales.models.NoSuchModelError:
            return error_response("unknown model {}".format(repr(model_name)))
        except whales.util.chess.InvalidPGNError:
            return error_response("invalid PGN")
        return normal_response({"pgn": new_pgn})
    return error_response("unknown command {}".format(repr(command)))
