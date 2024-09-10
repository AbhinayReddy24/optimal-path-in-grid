- How to start a new project 
 - create a folder 
 - create a virtual environment inside the folder command - python3 -m venv "virtual_environment_name"
 - activate the virtual environment:
    - On macOS/Linux: `source virtual_environment_name/bin/activate`
    - On Windows: `.\virtual_environment_name\Scripts\activate`
 - install new libraries command - pip install library_name
 - after installing everything freeze the requirments command - pip freeze > requirements.txt
 - if there is already requirments file the command - python3 -m pip install -r requirements.txt
 - start version control command - git init

 - I am too lazy to write project description (code is self explainatory and not super complicated)
 - Before judging Yes there can be lot of optimizations can be made in the code, 
   - but my priority is full  implementation
- Project successful commit is for optimal path in the grid

 - Update (08/09/2024) implemented version 3 closer to working compared to v2
   - issues with version 2 was that it is kind of min max algorithm rather than q learning
   - now q value is updated for the every move even for the move played by 0
   - in next update I will try to make it so that q table is updated sperately for X and O 
   - I think next update should be fully implemented version 
 
 - Update (09/092024) Potential discoveries
   - based on the fundamentals position 1,1  is the  position that should maximize the win  chances
   - if we are following epsilon greedy (not really huge fan) there is no opportunity 
       for the further more exploration of states that were partial wins 
       - example: lets say I want to explore 80% of the times when starting out 
          and for position started with 2,0 had first win after this 20% of the times this move would
          be picked there is bias towards that particular state (kind of achiving local minima)
       - POTENTIAL FIX: instead of doing e, 1-e in epsilon greedy we can do something like 
                  e(for new exploration), e1-e(re-exploring the successful states),
                  1-e1(explotiating successful state)
