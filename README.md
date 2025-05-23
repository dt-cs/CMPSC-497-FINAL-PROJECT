# EMBEDDING INTELLIGENCE IN 3D MODELING WORKFLOWS
 AN APPROACH FOR ADAPTING LANGUAGE MODELS TO ASSIST USERS IN 3D MODELING USING NATURAL LANGUAGE 

## 1. Overview

The progression of human civilization is inherently linked to the evolution of tools. Over the past century, architectural design has evolved alongside the development of computational tools and digital modeling environments that mediate creative production. 3D modeling remains an integral part of today's design process. However, the steep learning curve of 3D modeling applications, due to their complex user interfaces and extensive command sets, presents a significant barrier. In academic settings, students often dedicate considerable time to learning these tools, limiting their ability to focus on design exploration and development.

This research positions itself within this critical context and investigates how Large Language Models (LLMs) can be adapted to reimagine human-computer interaction in 3D modeling environments. It challenges conventional modeling methods by embedding an LLM within Rhinoceros 3D, enabling users to communicate their design intent using natural language through both text and voice inputs.

The key adaptation method for this purpose is fine-tuning the model on Rhino-specific data to generate executable Python scripts for complex modeling operations.

## 2. Goals and Objectives

This research aims to develop an LLM-based system that redefines how users interact with 3D modeling software by enabling natural language communication. By challenging conventional interface paradigms centered around command-line inputs, menus, and icons, the project seeks to make modeling tools more accessible, intuitive, and inclusive for diverse users, regardless of their technical expertise or physical abilities.

To accomplish this goal, the research will develop a framework for adapting general-purpose language models to 3D modeling workflows in Rhinoceros through instruction fine-tuning on Rhino-specific data.

## 3. Research Plan

### 3.1 Adapting Language Models for 3D Modeling Tasks

Pretrained language models, such as GPT, LLaMA, and CodeLLaMA, are optimized for general-purpose language generation and code synthesis tasks. However, these models are not inherently aligned with domain-specific requirements such as generating executable commands or scripts within a 3D modeling environment like Rhinoceros.

To adapt language models for 3D modeling tasks, this research employs instruction fine-tuning on a Rhino-specific dataset, consisting of modeling tasks paired with corresponding Python script responses. Fine-tuning enhances the model's ability to generate complex scripts for modeling tasks.

### 3.2 Challenges in Fine-tuning and Mitigation Strategy

Fine-tuning large-scale language models presents significant computational challenges, particularly when working with models containing billions of parameters. Moreover, adapting these models to domain-specific tasks increases the risk of catastrophic forgetting, wherein the model loses its general language understanding capabilities learned during pretraining.

To address these challenges, this research employs parameter-efficient fine-tuning (PEFT) techniques, specifically Low-Rank Adaptation (LoRA). LoRA introduces a small set of trainable low-rank matrices into the model architecture, enabling domain adaptation with reduced computational overhead while retaining the model's general language capabilities.

## 4. Dataset Construction for Instruction Fine-Tuning

### 4.1 Extracting Rhino-Specific Data

Rhino API documentation for Python scripting serves as the primary source of structured command data, including command names, parameters, descriptions, and example scripts. A Python program is developed to automate the extraction of this content using the BeautifulSoup library, outputting a structured JSON object containing command name, command description, parameters, and example script fields.

### 4.2 Synthesizing User Queries

To simulate real-world user interaction, synthetic queries are generated for each command. This process utilizes GPT-4o via OpenAI's API to generate four distinct types of user queries:

1. A beginner-level query describing the modeling goal without command knowledge
2. An intermediate query reflecting conceptual understanding but lacking technical specifics
3. An expert query referencing command names and parameters
4. A contextual query embedding the command within a specific design scenario or workflow

The synthetic user query, combined with the system prompt, forms the instruction component of the instruction-response pair.

### 4.3 Generating Python Script Responses

For each synthetic query, a corresponding Python script is generated to serve as the response component. This process uses GPT-4o with a structured system prompt, an example code template, and task descriptions to guide the model in generating accurate, executable Python scripts aligned with the Rhino API.

### 4.4 Compiling Instruction-Response Pairs

The final dataset is formatted in a conversational structure consistent with OpenAI's fine-tuning data specifications. This formatting enables the dataset to be directly utilized for supervised instruction fine-tuning. The dataset will be uploaded to the Hugging Face Hub for version control and subsequent access during model training.

```json
{
    "example": "Grid of Points in 3D Space",
    "instruction": "Generate a uniform 3D grid of points within a bounding box.",
    "reasoning": "Understanding spatial divisions helps lay the groundwork for any parametric modeling process.",
    "pseudocode": "1. Define bounding box dimensions (x_max, y_max, z_max).\n2. Set spacing interval (dx, dy, dz).\n3. For x in range(0, x_max, dx):\n  For y in range(0, y_max, dy):\n    For z in range(0, z_max, dz):\n      Place point at (x, y, z).",
    "python_procedural_algorithm": "\nimport rhinoscriptsyntax as rs\n# Request bounding box dimensions and spacing from user\nx_max = rs.GetReal('Enter bounding box X size')\ny_max = rs.GetReal('Enter bounding box Y size')\nz_max = rs.GetReal('Enter bounding box Z size')\ndx = rs.GetReal('Enter X spacing')\ndy = rs.GetReal('Enter Y spacing')\ndz = rs.GetReal('Enter Z spacing')\n# Use nested loops to iterate through the bounding box and add points\nx = 0.0\nwhile x <= x_max:\n    y = 0.0\n    while y <= y_max:\n        z = 0.0\n        while z <= z_max:\n            rs.AddPoint((x, y, z))  # Add a point at each grid location\n            z += dz\n        y += dy\n    x += dx\n"
  }
```

## 5. Supervised Fine-Tuning (SFT)

### 5.1 Model Selection

Large-scale language models containing over 100 billion parameters, while highly capable, present significant computational challenges for domain-specific fine-tuning and inference tasks. To balance model performance with computational efficiency, this research focuses on smaller-scale models ranging from 1 billion to 11 billion parameters, which can be hosted locally and fine-tuned with limited hardware resources.

This study employs the Gemma 3 27B model as the base model for supervised fine-tuning, selected for its open-source availability, instruction-tuned architecture, and compatibility with parameter-efficient fine-tuning techniques.

### 5.2 Fine-Tuning with Low-Rank Adaptation (LoRA)

Supervised fine-tuning will be conducted using the Hugging Face Transformers and PEFT libraries. The instruction-response dataset will be loaded into the training pipeline, with instruction text masked during training to calculate loss exclusively on the response generation.

LoRA introduces additional trainable low-rank matrices into specific layers of the model, enabling task-specific adaptation while preserving the general knowledge of the pretrained model. During inference, these low-rank adaptations are combined with the base model weights to generate output without modifying the full set of original parameters.

This approach significantly reduces training time, mitigates catastrophic forgetting, and facilitates efficient fine-tuning across different tasks. The number of training epochs will be determined based on validation performance and available computational resources.

![Learning Curve 02](learning%20curve/learning%20curve%2002.PNG)

# Learning Curve Analysis

## Epoch 1 vs Epoch 2
View the comparison between Epoch 1 and Epoch 2 [here](https://dt-cs.github.io/CMPSC-497-FINAL-PROJECT/learning-curve-comparison.html).

## Epoch 1 vs Epoch 2 vs Epoch 3
View the detailed comparison of three epochs [here](https://dt-cs.github.io/CMPSC-497-FINAL-PROJECT/three-epochs-comparison.html).

### 5.3 Sample response for a query

create a circle along a curve

```
### Reasoning & Steps
Rolling a circle along a curve generates a pipe-like form useful in railings, pipes, or architectural profiles.

1. Define a curve path.
2. Define a circle profile.
3. Sweep the circle along the curve.
4. Output the resulting pipe surface.

### Thinking
Analyzing the provided pseudocode and referencing the available RhinoPython functions...
To implement the above steps of creating a circle along a curve and generating a pipe-like form, the key operation is to sweep the circle profile along the curve path. This is typically done using the AddSweep1 function, which allows sweeping a rail curve with one or more rail curves and a shape curve. In this case, the curve path will be the rail curve, and the circle profile will be the shape curve. Therefore, the relevant RhinoPython function is:\n\nrs.AddSweep1(rail: list[guid], shapes: list[guid], closed: bool=False) -> guid"

### Code
```python
import rhinoscriptsyntax as rs

# Step 1: Get the curve path from the user
curve_path = rs.GetObject("Select the curve path", rs.filter.curve)

# Step 2: Get the circle profile from the user
circle_profile = rs.GetObject("Select the circle profile", rs.filter.curve)

# Step 3: Sweep the circle along the curve
if curve_path and circle_profile:
    # Sweep1 requires rail and shape curves
    # Rail is the curve path, shape is the circle profile
    pipe_surface = rs.AddSweep1(curve_path, [circle_profile], closed=False)
    if pipe_surface:
        rs.SelectObject(pipe_surface)
        rs.MessageBox("Pipe surface created successfully.")
    else:
        rs.MessageBox("Failed to create pipe surface.")
else:
    rs.MessageBox("Please select both a curve path and a circle profile.")
```
### 6. Discussion and Future Work

The analysis of the learning curve shows that the fine-tuned model has successfully learned to interpret natural language instructions for 3D modeling operations. The model demonstrates competency in parsing user inputs, decomposing complex modeling tasks into logical steps, creating pseudocode representations, and identifying appropriate function signatures within the Rhinoceros Python API. The significant reduction in training loss across both epochs (69.0% overall) indicates effective adaptation to the domain-specific task.
However, the model still exhibits limitations in its function generation capabilities. Specifically, it occasionally produces functions that do not exist within the RhinoPython library ecosystem, creating theoretically sound but practically non-executable code. This discrepancy highlights a gap between the model's general code generation abilities and its domain-specific knowledge of the Rhinoceros Python API constraints.
To address this limitation, implementing Direct Preference Optimization (DPO) as the next refinement stage could substantially improve performance. DPO represents an advancement over traditional reinforcement learning from human feedback methods by directly optimizing the preference gap between desired and undesired outputs without requiring an explicit reward model. The implementation would involve:

Generating paired samples of responses (correct RhinoPython functions vs. invalid functions) for identical user queries
1. Formulating a preference dataset where valid RhinoPython API implementations are preferred over invalid ones
2. Optimizing the model to maximize the likelihood gap between preferred and non-preferred responses

This approach would effectively penalize the model for generating non-existent functions while reinforcing the use of valid RhinoPython API calls.
