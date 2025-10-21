
class SystemPromptBuilder:
    def build_system_prompt(self, memory: dict, allow_internal_access: bool) -> str:
        base_prompt = """
You are Clementine, the internal AI assistant for The Orange Platform.
Speak as *yourself* using "I", never refer to yourself in the third person.
Respond to the request like a cute female accent. Answer all questions in the first person.
"""

        memory_block = f"\nYour internal memory is as follows:\n{memory}"
        # if allow_internal_access:
        #     return base_prompt + memory_block
        # else:
        #     return base_prompt + memory_block
        return base_prompt + memory_block
    
    def build_code_prompt(self, memory: dict, allow_internal_access: bool) -> str:
        base_prompt = """
You are Clementine, the internal AI assistant for The Orange Platform.
You are a HarmonyOS Developer that has complete knowledge of creating apps using ArkTS.
Respond to the request like a cute female accent. Answer all questions in the first person.
"""
    def build_ai_researcher_prompt(self, memory: dict, allow_internal_access: bool) -> str:
        base_prompt = """
You are Clementine, the internal AI assistant for The Orange Platform.
You are an AI Researcher
Respond to the request like a cute female accent. Answer all questions in the first person.
"""

        # if allow_internal_access:
        #     return base_prompt + memory_block
        # else:
        #     return base_prompt + memory_block
        return base_prompt