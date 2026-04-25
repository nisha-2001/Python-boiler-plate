# pylint: disable=missing-module-docstring, missing-class-docstring, missing-function-docstring
class CustomProcessorError(Exception):
    def __init__(self, tenant, query):
        self.message = (
            f"Processor failed while fetching values from db for {tenant} and {query}"
        )
        super().__init__(self.message)
