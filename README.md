InSights: Generating Visualizations with Natural Language Guidance
Harness the power of large language models to create data visualizations using natural language prompts!

Overview
This Streamlit web app enables you to:

Upload a CSV file containing your data
Describe what you want to visualize using natural language
See the generated visualization code and the resulting visual representation
It leverages the powerful Llama 2 language model to translate your natural language prompts into visualization code, leveraging Plotly for rendering.

Key Features
Intuitive interface: Explore your data with simple prompts, no coding required.
Leverages Llama 2: Harnesses the capabilities of a large language model for natural language understanding and code generation.
Visualization flexibility: Generates code for various Plotly visualizations based on your prompts.
Customizable styling: Includes a CSS file (style.css) for tailoring the app's appearance.
Installation and Setup
Clone this repository:

Bash
git clone https://github.com/thekakodkar/insight-app
Use code with caution.
Install required libraries:

Bash
cd insight-app
pip install -r requirements.txt
Use code with caution.
Download Llama 2 model:

Obtain the Llama 2 model files (version "model/llama2") from the Hugging Face model hub: [invalid URL removed]
Place the model files in the "model/llama2" directory within this project.
Running the App
Start Streamlit:

Bash
streamlit run app.py
Use code with caution.
Access the app in a web browser:
Typically at http://localhost:8578 or the address specified by Streamlit.

Usage
Upload a CSV file: Click "Choose a CSV file" and select your data.
Provide a prompt (optional): Optionally, enter a natural language description to summarize your data.
Generate visualization: Enter a natural language prompt describing the visualization you desire (e.g., "Create a bar chart showing the distribution of sales by country").
Review generated code: The app displays the generated Plotly visualization code.
View visualization: Explore the resulting interactive visualization.
Customization
Styling: Adjust the visual appearance by modifying the style.css file.
Summary function: Replace the placeholder summary function with a more tailored approach for your specific needs.

Contributing
We welcome contributions! Feel free to open issues or pull requests.

License
This project is licensed under the MIT License: LICENSE.