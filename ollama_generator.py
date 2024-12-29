import ollama
import yaml

class OllamaGenerator:
    def __init__(self, config_path='config.yaml'):
        with open(config_path, 'r') as file:
            self.config = yaml.safe_load(file)
    
    def generate_topic(self):
        """Generate an engaging topic for the reel"""
        response = ollama.generate(
            model=self.config['ollama']['model'], 
            prompt=self.config['ollama']['preprompt'],
            options={
                'temperature': self.config['ollama']['temperature'],
                'num_predict': self.config['ollama']['max_tokens']
            }
        )
        return response['response']
    
    def generate_script(self, topic):
        """Generate a concise, engaging script for the topic"""
        script_prompt = f"""
        Create a concise, engaging 30-60 second script about this topic:
        {topic}

        Guidelines:
        - Write in a direct, informative, and captivating style
        - Use clear, impactful language
        - Start with a compelling fact or insight
        - Maintain a conversational yet authoritative tone
        - Aim for approximately 150-250 words
        - Conclude with a memorable takeaway or insight
        - Avoid cinematic directions or staging instructions
        """
        
        response = ollama.generate(
            model=self.config['ollama']['model'], 
            prompt=script_prompt,
            options={
                'temperature': 0.7,
                'num_predict': 300
            }
        )
        return response['response']

def main():
    generator = OllamaGenerator()
    topic = generator.generate_topic()
    script = generator.generate_script(topic)
    print("Generated Topic:", topic)
    print("\nGenerated Script:\n", script)

if __name__ == "__main__":
    main()
