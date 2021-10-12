int numRootBranches = 3;
Branch[] rootBranches = new Branch[numRootBranches];

void setup() {
    size(800,400);
    // frameRate(5);
    colorMode(HSB, 360, 100, 100);
    for (int i = 0; i < numRootBranches; i++) {
        rootBranches[i] = new Branch(400, 200);
    }
}

void draw() {
    background(0);
    
    //draw branches
    for (Branch b : rootBranches) {
        b.saveArc();
        b.displayArc();
    }
	// noLoop();
}
