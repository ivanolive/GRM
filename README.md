# GRM
Group Regularity Mobility Model

Research Paper: https://arxiv.org/pdf/1706.07908.pdf

# Citation Information (bibtex): 
```latex
@INPROCEEDINGS{
    grm,
    AUTHOR="Ivan Nunes and Clayson Celes and Michael Silva and Pedro {Vaz de Melo} and Antonio {A.F. Loureiro}",
    TITLE="{GRM:} Group Regularity Mobility Model",
    BOOKTITLE="20th ACM International Conference on Modeling, Analysis and Simulation of Wireless and Mobile Systems (MSWiM'17)",
    ADDRESS="Miami Beach, USA",
    YEAR=2017
}
```


GRM is a novel mobility model that accounts for the role of group meeting dynamics and regularity in human mobility. Previous mobility models do not capture the regularity of human group meetings, an important aspect that should be included by synthetic  mobility modeling since it is present in real mobility traces. Based on the characterization of statistical properties of group meetings in real mobility traces we have designed GRM. GRM maintains the typical pairwise contact properties of other synthetic models in the literature, such as contact duration and inter-contact time distributions. In addition, GRM accounts for the role of group mobility, presenting group meetings regularity and social communities structure. Mobility traces generated by GRM are fully compliant and ready to run on The ONE Simulator for opportunistic networks (https://akeranen.github.io/the-one/).

# READY TO GO MOBILITY TRACES
If you want to skip the trouble of setting up and running the code yourself to generate your own mobility traces, ready-to-go GRM mobility traces containing 100, 1000, and 2000 mobile nodes trajectories, throughout a period of 2 months, are available together with a demo video of GRM working on top of The ONE Simulator at:

https://www.dropbox.com/sh/792mi849nf3dvam/AAAR4RofaLBfoFaxmeONe-H4a?dl=0

# DEPENDENCIES
- Python 2.7, 3.3 or later.
- NetworkX 1.11 or later.
- Numpy 1.8.2 or later.
- Matplotlib 1.3.1 or later.

# RUNNING
The RegDistro.csv file specifies the number of groups (column 1) and their respective meeting regularity (column 2). Other simulation parameters can be configured inside main.py source. Please refer to GRM paper for details on the simulation parameters.

- Option 1: "python main.py" -- uses synthetic social graph
- Option 2: "python main.py path_to_social_net_spec_file" -- uses any specified social graph

OUTPUT TRACES:

- sorted_trace.csv : nodes mobility sorted by time (compatible with The ONE Simulator)
- trace.csv : nodes mobility sorted by node ID
- contacts_test.csv : pairwise proximity contacts due to social group meetings. Coincidental contacts, due to intersections of individual trajectories are not listed in this file.
Format: "ID1 ID2 CONTACT-TIME CONTACT-DURATION"

