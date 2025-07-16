class UserMessageHandler:
    def __init__(self, llm, prompt):
        self.llm = llm
        self.prompt = prompt

    def process(self, message: str) -> str:
        """
        사용자의 메시지를 LLM으로 처리하여 벡터 스토어 쿼리 품질 개선
        """
        runnable = self.prompt | self.llm
        processed_message = runnable.invoke({"input": message})

        return processed_message
