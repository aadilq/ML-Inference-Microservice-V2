# ML-Inference-Microservice-V2

The ml-inference-microservice is an evolution of the ai-editor-pipeline (see github repo below) where the Scoring logic has been transformed into a standalone ML inference microservice. In the previous iteration of the project, we used Claude API with a custom system prompt to score the each video snippet. Now, we will use Zero-Shot-Classification from Huggingface to create our standalone scoring microservice. The whole idea is to integrate an ML model into the production pipeline we just created, so that it can scale independently. 



