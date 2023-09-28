from neo4j import GraphDatabase
from dotenv import load_dotenv

class Importer:

    #init local connection to database
    def __init__(self):

        load_dotenv()

        NEO4J_URI = "bolt://localhost:7687"
        NEO4J_USER = 'neo4j'
        NEO4J_PASSWORD = 'password'

        self.driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

    #close connection to database
    def close(self):
        self.driver.close()
    
    #inserts everything into the databse
    def create_db(self, file, features, labels):
        with open(file, 'r') as f:
            lines = f.readlines()
            for line in lines[1:]:
                values = line.strip().split('\t')
                user_id = int(values[1])
                target_id = int(values[2])
                #whenever you encounter a user that does not exist, add them to the base
                if not self.check_if_user_exists(user_id):
                    self.create_user(user_id)
                    print("User created: ", user_id)
                #whenever you encounter a target that does not exist, add them to the base
                if not self.check_if_target_exists(target_id):
                    self.create_target(target_id)
                    print("Target created: ", target_id)
                action_id = int(values[0])
                timestamp = float(values[3])
                label = labels[action_id]
                f0 = features[0][action_id]
                f1 = features[1][action_id]
                f2 = features[2][action_id]
                f3 = features[3][action_id]
                #create the edge between the user and the target
                self.create_action(action_id, user_id, target_id, timestamp, label, f0, f1, f2, f3)
                print("Action created:{} -> {} ".format(user_id, target_id))
    
    #purge the db to start anew
    def purge_db(self):
        self.driver.execute_query("MATCH (n) DETACH DELETE n")
        return
    
    #check if the user with id @user_id exists
    def check_if_user_exists(self, user_id):
        query = '''MATCH (u:User WHERE u.id = $id) RETURN count(u) as count'''
        result = self.driver.execute_query(query, id=user_id)
        #the result is gonna be <Record count=1> or <Record count=0>, so we just check if 1 is in the result
        if 1 in result[0][0]:
            return True
        return False
    
    #check if the target with id @target_id exists
    def check_if_target_exists(self, target_id):
        query = '''MATCH (t:Target WHERE t.id = $id) RETURN count(t) as count'''
        result = self.driver.execute_query(query, id=target_id)
        #the result is gonna be <Record count=1> or <Record count=0>, so we just check if 1 is in the result
        if 1 in result[0][0]:
            return True
        return False

    #create a user with id @user_id
    def create_user(self, user_id):
        self.driver.execute_query("CREATE (u:User {id: $id})", id=user_id)
    
    #create a target with id @target_id
    def create_target(self, target_id):
        self.driver.execute_query("CREATE (t:Target {id: $id})", id=target_id)

    #create an action with id @action_id, between user with id @user_id and target with id @target_id
    def create_action(self, action_id, user_id, target_id, timestamp , label , f0 , f1 , f2 , f3):
        self.driver.execute_query(
                    query_="""MATCH (u:User{id :""" + str(user_id) + """}) , (t:Target{id:""" + str(target_id) + """})
                            CREATE (u) - [:TAKE_ACTION{timestamp:""" + str(timestamp) + """ , ACTIONID:""" + str(action_id) + """ 
                            , LABEL:""" + str(label)+ """, FEATURE0:""" + str(f0) + """ , FEATURE1:""" + str(f1)+ """
                            , FEATURE2:""" + str(f2) + """ , FEATURE3:""" + str(f3) + """  }] -> (t)"""
            )

    #load the labels of all actions from the file
    def load_labels(self, file):
        labels = []
        with open(file, 'r') as f:
            lines = f.readlines()
            for line in lines[1:]:
                values = line.strip().split('\t')
                label = int(values[1])
                labels.append(label)
        return labels
    
    #load the features of all actions from the file
    def load_features(self, file):
        feature0, feature1, feature2, feature3 = [], [], [], []
        with open(file, 'r') as f:
            lines = f.readlines()
            for line in lines[1:]:
                values = line.strip().split('\t')
                feature0.append(float(values[1]))
                feature1.append(float(values[2]))
                feature2.append(float(values[3]))
                feature3.append(float(values[4]))
        features = [feature0, feature1, feature2, feature3]
        return features

if __name__ == "__main__":
    db = Importer()
    print("Connected to database")
    db.purge_db()
    print("Database purged")
    features = db.load_features('../data/mooc_action_features.tsv')
    print("Features imported")
    labels = db.load_labels('../data/mooc_action_labels.tsv')
    print("Labels imported")

    db.create_db('../data/mooc_actions.tsv', features, labels)
