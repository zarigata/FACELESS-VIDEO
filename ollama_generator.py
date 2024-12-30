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
        Generate ONLY the spoken script text for a 30-second educational video about this topic:
        {topic}

        Requirements:
        - Provide ONLY the exact words to be spoken
        - No stage directions, visual descriptions, or formatting
        - Write in a clear, engaging, conversational tone
        - Focus on delivering key information concisely
        - Aim for approximately 150-250 words
        - Ensure the script can be read in about 30 seconds
        - Use language that sounds natural when spoken aloud

        Output ONLY the raw script text."""
        
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
