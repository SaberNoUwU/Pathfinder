# **PATHFINDER** 

Here is my small project I code in Python. 

This project uses few algorithms including Visibility Graph and Djikstra to find the shortest path between 2 points in a preset maze. 

*__Features__*:
- Scroll bar (Horizontal + Vertical) 
- Zoom-in / Zoom-out
- Multiple copies of the map


To start the project, follow these steps: 

1) **Download to your Python library necessary modules**:
   
`pip install -r requirements.txt` 

**NOTES**: For Debian/Ubuntu users, I recommend install those modules to your virtual environment (venv)


2) **Start the project**

`python3 MazeFinder.py` 


To use the project, follow these steps: 

1) Generate a map by sliding _Repeat Time_ slider\
**Note**: Recommend combining with sliding _Grid Size_ slider to make the size of the graphs bigger.

2) Pick two points, _Start Point_ and _End Point_, by their respective buttons. 

3) Create the Visibility Graph using _Visibility Graph_ button.

4) And finally, Calculate the shortest distance between two points using _Calculate_ button. 

**NOTES**: 
- You can show the Visbility Graph at the Start Point and at the End Point using the _Show SVisib_ and _Show EVisib_ buttons (Should turn off the Visibility Graphs when you finish watching it by clicking on the same buttons).
- **MAKE SURE** to reset the program by using _Clear Path_ button.
- You can use two scroll bars on the top-right side to scroll up or down (Vertical) or left or right (Horizontal).
