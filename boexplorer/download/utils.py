from random_user_agent.user_agent import UserAgent

user_agent_rotator = UserAgent()

def get_random_user_agent():
    return user_agent_rotator.get_random_user_agent()
