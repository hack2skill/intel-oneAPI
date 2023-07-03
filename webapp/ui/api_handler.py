import requests

from utils.logging_handler import Logger


class PredictAskDoubt(object):
    """Class to use AskDoubt API"""

    def __init__(self, server_config):
        self.server_config = server_config

    # @st.cache_data
    def predict_ask_doubt(self, payload):
        """POST request"""
        
        url = "http://{}:{}/leap/api/v1/ask-doubt".format(
            self.server_config["server_host"],
            self.server_config["server_port"])

        Logger.info(f"Sending request to {url}")
        Logger.info(f"Request payload: {payload}")
        response = requests.post(url=url,
                                 headers={
                                     'Content-Type': 'application/json',
                                 },
                                 json=payload)
        Logger.info("Response: {response}")
        processed_response = self._process_response(response=response)
        Logger.info(f"Processed Response: {processed_response}")
        return processed_response

    def _process_response(self, response):
        """Checks for API errors and returns a processed response.
        Response will be a triplet containing answer, context, and meta-data.

        Args:
            response (_type_): _description_

        Returns:
            _type_: _description_
        """
        if response.status_code == 200:
            data = response.json()
            results = data["data"]
            return self._find_answer(results)
        else:
            Logger.error("Error Message:", response.text)
            return "Could not find answer, check your network...", None, None

    def _find_answer(self, results):
        """Processes response to get answer, context, and any meta-data for response.

        Args:
            results (_type_): _description_

        Returns:
            _type_: _description_
        """
        answer = results['answer']
        relevant_context_id = results['relevant_context_id']
        if answer:
            if relevant_context_id > -1:
                relevant_context = results['relevant_contexts'][relevant_context_id]
                return answer, relevant_context['context'], relevant_context['metadata']
            else:
                return answer, None, None
        else:
            return "Sorry, I couldn't find an answer in course material", None, None

class PredictAIExaminer(object):
    """Class to use AIExaminer API"""

    def __init__(self, server_config):
        self.server_config = server_config

    def predict_aiexaminer_ask_question(self, payload):
        """POST request"""
        url = "http://{}:{}/leap/api/v1/ai-examiner/ask-question".format(
            self.server_config["server_host"],
            self.server_config["server_port"])
        response = requests.post(url=url,
                        headers={
                            'Content-Type': 'application/json',
                        },
                        json=payload).json()

        return response
    
    def predict_aiexaminer_eval_answer(self, payload):
        """POST request"""
        url = "http://{}:{}/leap/api/v1/ai-examiner/eval-answer".format(
            self.server_config["server_host"],
            self.server_config["server_port"])
        response = requests.post(url=url,
                        headers={
                            'Content-Type': 'application/json',
                        },
                        json=payload).json()

        return response
    
    def predict_aiexaminer_hint_motivate(self, payload):
        """POST request"""
        url = "http://{}:{}/leap/api/v1/ai-examiner/hint-motivate".format(
            self.server_config["server_host"],
            self.server_config["server_port"])
        response = requests.post(url=url,
                        headers={
                            'Content-Type': 'application/json',
                        },
                        json=payload).json()

        return response