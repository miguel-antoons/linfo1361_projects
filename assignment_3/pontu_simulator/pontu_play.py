from pontu_tools import *

if __name__ == '__main__':
  agent0 = "human_agent"
  agent1 = "human_agent"

  initial_state = PontuState()
  agent0 = getattr(__import__(agent0), 'MyAgent')()
  agent0.set_id(0)
  agent1 = getattr(__import__(agent1), 'MyAgent')()
  agent1.set_id(1)
  res = make_match(initial_state, [agent0, agent1], None, True, None)
  print(res)
