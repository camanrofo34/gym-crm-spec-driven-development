# Frontend iteration of the Spec Driven Development

## Why doing a frontend iteration?

The real reason to do a frontend iteration was... Just I felt that it was so bad to present only the server :c

Well, a real reason could be that in a Spec Driven Development, it's nearly correct that when the server it's already developed
with specifications and validation, the next step should be doing the frontend so it can be a complete monolith or 
client-server architecture.

## Generating the Requirement List (or the visual?):

In this case, the requirement list stays the same as the original, due to the type of implementation this second iteration is.

The real impact appears on the prompt, that can be found in: [Prompt Frontend](../prompts/prompt_frontend.md ).

This second prompt works as it's the first on any other project because it doesn't use the already created python endpoints.
It only uses the original specification used to generate the API in python, so this isn't a refinement of the original idea,
otherwise, it's an addition to it.

In this way, the connection and the usage of the frontend is the way to validate many things, such as the backend work,
the connection, and the complete flow of the requirements.

## It worked?

So, the short answer is, yes, it worked. All the functionalities expected were running on the frontend with a good 
visual. But in the long term the answer should be no...

The backend works as the way it works, using unique identification to join the related users (trainer or trainees) so the 
query doesn't consume N+1 operations while searching by the name, or around all the pages. However, normally (in the times I
used any AI model for the front generation), it doesn't take into account that the actual user doesn't know anything about
internal identification, so it should prefer around pickers with friendly data like name (or at least common identificators
like the NIT or the 'cedula').

So the idea of usability isn't the best, but inside the prompt and the expected task, it worked :D