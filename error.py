# from starlette.applications import Starlette
# from flask import jsonify
# from starlette.requests import Request
# from werkzeug.exceptions import BadRequest
# from starlette.responses import JSONResponse
# from starlette.exceptions import HTTPException
# from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR, HTTP_422_UNPROCESSABLE_ENTITY
# import logging
# import traceback
#
# # Настройка логгера
# logging.basicConfig(level=logging.ERROR)
# logger = logging.getLogger(__name__)
#
#
# async def http_exception_handler(request: Request, exc: HTTPException):
#     print('hu')
#     return JSONResponse(
#         status_code=exc.status_code,
#         content={
#             "message": exc.detail,
#             "success": False,
#             "error": exc.__class__.__name__,
#         },
#     )
#
#
# async def validation_exception_handler(request: Request, exc: BadRequest):
#     print('huuuuii')
#     return jsonify(
#         status_code=HTTP_422_UNPROCESSABLE_ENTITY,
#         content={
#             "message": "Ошибка валидации данных",
#             "errors": exc.description,
#             "success": False,
#             "error": exc.__class__.__name__,
#         },
#     )
#
#
# async def python_exception_handler(request: Request, exc: Exception):
#     logger.error(
#         f"Необработанное исключение: {exc}\n"
#         f"Запрос: {request.method} {request.url}\n"
#         f"Трассировка: {traceback.format_exc()}"
#     )
#
#     return jsonify(
#         status_code=HTTP_500_INTERNAL_SERVER_ERROR,
#         content={
#             "message": "Внутренняя ошибка сервера",
#             "success": False,
#             "error": exc.__class__.__name__,
#         },
#     )
#
#
# def setup_exception_handlers(app: Starlette):
#     app.add_exception_handler(HTTPException, http_exception_handler)
#     app.add_exception_handler(BadRequest, validation_exception_handler)
#     app.add_exception_handler(Exception, python_exception_handler)
