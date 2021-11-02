int numRootBranches = 1;
Branch[] rootBranches = new Branch[numRootBranches];

void setup() {
    size(800,400);
    frameRate(1);
    colorMode(HSB, 360, 100, 100);
    for (int i = 0; i < numRootBranches; i++) {
        rootBranches[i] = new Branch(400, 200, 0);
    }
}

void draw() {
    background(0);

    for (Branch branch : rootBranches) {
        // random direction for the arc to go towards
        PVector desiredDirectionVector = PVector.random2D();
        // create all the branches
        branch.saveArc(desiredDirectionVector);
        // calc the furthest point to use lerping
        float rootBranchFurthestDist = branch.calcFurthestDist();
        // draw the glow parts of the branch
        branch.drawArcGlow(5);
        // draw the main white part of the branch
    }
    // noLoop();
}