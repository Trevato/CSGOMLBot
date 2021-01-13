from http.server import BaseHTTPRequestHandler, HTTPServer
import sys
import time
import json
import requests
import pprint


class CSGOGameStateServer(HTTPServer):

    def __init__(self, server_address, auth_token):

        super(MyServer, self).__init__(server_address, CSGOGameStateRequestHandler)
        self.auth_token = auth_token


    def add_reward(self, n):
        self.reward = self.reward + n
        # print(self.reward)

    def get_reward(self):
        # print('get_reward')
        return self.reward

    def reset_reward(self):
        self.reward = 0


class CSGOGameStateRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        # print(self.headers)
        length = int(self.headers['Content-Length'])
        body = self.rfile.read(length).decode('utf-8')
        # print(body)
        # print('\n\n')
        # print(pprint.pprint(self.responses))
        # print('\n\n')

        self.parse_gamestate_payload(json.loads(body))

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def is_payload_authentic(self, payload):

        with open('allPayloadExample.json', 'a') as outfile:
            json.dump(payload, outfile)
        #Get auth token and redirect packet to correct function
        if 'auth' in payload and 'token' in payload['auth']:
            return 'gamestate'
        elif 'auth' in payload and 'frameSync' in payload['auth']:
            return 'frameSync'
        else:
            return False

    def parse_gamestate_payload(self, payload):
        if not self.is_payload_authentic(payload) == 'gamestate':
            return None


        #Local variables for temp payload saving using functions below
        round_phase = self.get_round_phase(payload)
        name = self.get_player_name(payload)
        kills = self.get_player_kills(payload)
        deaths = self.get_player_deaths(payload)
        health = self.get_player_health(payload)
        score = self.get_player_score(payload)
        team = self.get_player_team(payload)
        team_score = self.get_player_team_score(payload)
        opponent_team_score = self.get_player_opponent_team_score(payload)
        match_win = self.get_match_win(payload)

        #If there was a change then adjust server data
        #Also add reward
        if round_phase != self.server.round_phase:
            self.server.round_phase = round_phase

        if team != self.server.team:
            self.server.team = team

        if team_score != self.server.team_score:
            self.server.team_score = team_score
            self.server.reward += self.server.round_win_reward
            self.server.total_reward += self.server.round_win_reward

        if opponent_team_score != self.server.opponent_team_score:
            self.server.opponent_team_score = opponent_team_score
            self.server.reward += self.server.round_loss_reward
            self.server.total_reward += self.server.round_loss_reward

        if name != self.server.name:
            self.server.name = name

        if kills != self.server.kills:
            self.server.kills = kills
            self.server.reward += self.server.kill_reward
            self.server.total_reward += self.server.kill_reward

        if deaths != self.server.deaths:
            self.server.deaths = deaths
            self.server.reward += self.server.death_reward
            self.server.total_reward += self.server.death_reward

        if health != self.server.health:
            self.server.health = health

        if score != self.server.score:
            self.server.score = score

        if match_win != self.server.match_win:
            self.server.match_win = match_win

        self.server.add_reward(self.server.reward)
        # print(self.server.reward)

    #Functions to get data from payload
    def get_round_phase(self, payload):
        if 'round' in payload and 'phase' in payload['round']:
            return payload['round']['phase']
        else:
            return None

    def get_player_health(self, payload):
        if 'player' in payload and 'state' in payload['player'] and 'health' in payload['player']['state']:
            return payload['player']['state']['health']
        else:
            return None

    def get_player_kills(self, payload):
        if 'player' in payload and 'match_stats' in payload['player'] and 'kills' in payload['player']['match_stats']:
            return payload['player']['match_stats']['kills']
        else:
            return None

    def get_player_deaths(self, payload):
        if 'player' in payload and 'match_stats' in payload['player'] and 'deaths' in payload['player']['match_stats']:
            return payload['player']['match_stats']['deaths']
        else:
            return None

    def get_player_score(self, payload):
        if 'player' in payload and 'match_stats' in payload['player'] and 'score' in payload['player']['match_stats']:
            return payload['player']['match_stats']['score']
        else:
            return None

    def get_player_name(self, payload):
        if 'player_id' in payload and 'name' in payload['player_id']:
            return payload['player_id']['name']
        else:
            return None

    def get_player_team(self, payload):
        if 'player_id' in payload and 'team' in payload['player_id']:
            return payload['player_id']['team']
        else:
            return None

    def get_player_team_score(self, payload):
        if 'map' in payload and ('team_' + str(self.server.team)) in payload['map']:
            return payload['map']['team_' + str(self.server.team)]
        else:
            return None

    def get_player_opponent_team(self, payload):
        if self.server.team == 'T':
            return 'CT'
        elif self.server.team == 'CT':
            return 'T'
        else:
            return None

    def get_match_win(self, payload):
        if self.server.opponent_team_score == 16:
            self.server.match_win = False
            self.server.reward += self.server.match_loss_reward
        elif self.server.team_score == 16:
            self.server.match_win = True
            self.server.reward += self.server.match_win_reward

    def get_player_opponent_team_score(self, payload):
        if 'map' in payload and ('team_' + str(self.server.opponent_team)) in payload['map']:
            return payload['map']['team_' + str(self.server.opponent_team)]
        else:
            return None

    def log_message(self, format, *args):
        """
        Prevents requests from printing into the console
        """
        return

def start_server():

    print(time.asctime(), '-', 'CS:GO gamestate server starting')

    try:
        CSGOGameStateServer.serve_forever()
    except (KeyboardInterrupt, SystemExit):
        print('Server unable to start!')
        pass

    server.server_close()

if __name__ == '__main__':
    print('Main called.')
