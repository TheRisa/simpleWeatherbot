from rasa_nlu.training_data import load_data
from rasa_nlu.config import RasaNLUModelConfig
from rasa_nlu.model import Trainer
from rasa_nlu import config
from rasa_nlu.model import Metadata, Interpreter

def train_nlu(data, cfg, model_dir):
    training_data = load_data(data)
    cfg = config.load(cfg)
    trainer = Trainer(cfg)
    trainer.train(training_data)
    model_directory = trainer.persist(model_dir, fixed_model_name='weathernlu')

def run_nlu():
    interpeter = Interpreter.load('./models/nlu/default/weathernlu')
    print(interpeter.parse(u"What's the weather in Rome?"))


if __name__=='__main__':
    train_nlu('./data/data.json', 'config_spacy.json', './models/nlu')
    run_nlu()
    
