import pygame
from agent import Agent

class MyAgent(Agent):


	"""
	    This function transcripts the actions (the clicks) of a human agent into a valid action.

	    state: the current state
	    time_left: the number of second left

	    """
	def get_action(self, state, last_action, time_left):
		select_pawn = False
		pawn_id = None
		moved_pawn = False
		dir = None
		select_bridge = False
		action = None
		actions = state.get_current_player_actions()
		valid_pawns = []

		if actions[0][0] is None:
			# If no pawn can be moved but the player has not losed yet, pass directly to the removal of a bridge
			select_pawn = True
			moved_pawn = True
		else:
			# Add in the valid_pawns list the id of the current player's pawns than can move this round
			for action in actions:
				if action[0] not in valid_pawns:
					valid_pawns.append(action[0])

		if not select_pawn:
			print('select a valid pawn')

		while not select_pawn: # Iterate until the human has selected a valid pawn
			for event in pygame.event.get():
				if event.type == pygame.MOUSEBUTTONUP:
					pos = pygame.mouse.get_pos()
					x = int(pos[0]/50)
					y = int(pos[1]/50)
					if x < state.size * 2 - 1 and y < state.size * 2 - 1: # Check that the human clicked on the board
						if x % 2 == 0 and y % 2 ==0: # Check that the human clicked on an isle
							x = x/2
							y = y/2
							for i in range(state.size-2): # Check that the human clicked on a isle with a valid pawn on it
								if i in valid_pawns and (x,y) == state.get_pawn_position(state.cur_player,i):
									select_pawn = True
									pawn_id = i
									print('pawn selected')

				if event.type == pygame.QUIT:
					pygame.quit() 
					exit(0)

		if not moved_pawn:
			print('select a valid destination for your pawn')

		while not moved_pawn: # Iterate until the human has selected a destination for the selected pawn
			for event in pygame.event.get():
				if event.type == pygame.MOUSEBUTTONUP:
					pos = pygame.mouse.get_pos()
					x = int(pos[0]/50)
					y = int(pos[1]/50)
					if x < state.size * 2 - 1 and y < state.size * 2 - 1: # Check that the human clicked on the board
						if x % 2 == 0 and y % 2 ==0: # Check that the human clicked on an isle
							x = x/2
							y = y/2
							(X,Y) = state.get_pawn_position(state.cur_player, pawn_id)
							adj_bridges = state.adj_bridges(state.cur_player, pawn_id)
							adj_pawns = state.adj_pawns(state.cur_player, pawn_id)
							# Check that the human clicked on a valid destination isle
							if x == X - 1 and y == Y and adj_bridges[0] and not adj_pawns[0]:
								moved_pawn = True
								dir = 'WEST'
								print('destination selected')
							elif x == X and y == Y - 1 and adj_bridges[1] and not adj_pawns[1]:
								moved_pawn = True
								dir = 'NORTH'
								print('destination selected')
							elif x == X + 1 and y == Y and adj_bridges[2] and not adj_pawns[2]:
								moved_pawn = True
								dir = 'EAST'
								print('destination selected')
							elif x == X and y == Y + 1 and adj_bridges[3] and not adj_pawns[3]:
								moved_pawn = True
								dir = 'SOUTH'
								print('destination selected')

				if event.type == pygame.QUIT:
					pygame.quit()
					exit(0)

		if not select_bridge:
			print('select a bridge to remove')

		while not select_bridge: # Iterate until the human has selected a valid bridge to remove
			for event in pygame.event.get():
				if event.type == pygame.MOUSEBUTTONUP:
					pos = pygame.mouse.get_pos()
					x = int(pos[0]/50)
					y = int(pos[1]/50)
					if x < state.size*2 - 1 and y < state.size*2 - 1: # Check that the human clicked on the board
						if x % 2 == 1 and y % 2 == 0: # Check if the human clicked on a horizontal bridge
							x = int((x-1)/2)
							y = int(y/2)
							if state.h_bridges[y][x]: # Check if the bridge is still present
								select_bridge = True
								action = (pawn_id,dir,'h',x,y)
						elif x % 2 == 0 and y % 2 == 1: # Check if the human clicked on a vertical bridge
							x = int(x / 2)
							y = int((y  - 1) / 2)
							if state.v_bridges[y][x]: # Check if the bridge is still present
								select_bridge = True
								action = (pawn_id, dir, 'v', x, y)

				if event.type == pygame.QUIT:
					pygame.quit()
					exit(0)
		return action
  
	def get_name(self):
		return "human_agent"