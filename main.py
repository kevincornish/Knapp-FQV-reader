import random
import pickle

def create_dummy_results():
    inspectors = {}
    for number_of_inspectors in range(1, 6):
        for number_of_runs in range(1, 11):
            inspections = 1
            number_of_inspections = 250
            while inspections < number_of_inspections:
                results = {
                    f"inspector{number_of_inspectors}_{number_of_runs}_{inspections}": f"{random.randint(0,10)}"
                }
                inspectors.update(results)
                inspections += 1

    #store the dict in a pkl file
    with open("manual_data.pkl", "wb") as fp:
        pickle.dump(inspectors, fp)


def load_results():
    with open("manual_data.pkl", "rb") as fp:
        inspections = pickle.load(fp)
        print(inspections)
        #print(inspections["inspector1_6_9"])


#create_dummy_results()
load_results()
