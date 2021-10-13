class Branch {
    PVector startCoords;
    int recursionDepth;
    Branch[] daughterBranches;
    int numDaughterBranches;
    int numElectrons;
    PVector[] electronPath;
    float theta;
    float plusMinusTheta = PI/16;

    Branch(int x, int y, int numElecs, int recDepth) {
        startCoords = new PVector(x, y)
        recursionDepth = recDepth;
        numElectrons = numElecs;
        electronPath = new PVector[numElectrons];
        switch (recursionDepth) {
            case 0:
                numDaughterBranches = random(1,3);
                break;
            case 1:
                numDaughterBranches = random(0,3);
                break;
            case 2:
                numDaughterBranches = random(0,1);
                break;
            default:
                numDaughterBranches = 0;
        }

        if (numDaughterBranches != 0) {
            daughterBranches = new branch[numDaughterBranches];
        }
    }

    void saveArc() {
        // make the main arc
        PVector curCoords = startCoords.copy();
        PVector desiredDirectionVector = PVector.random2D();

        for (int i = 0; i < numElectrons; i++) {
            theta = random(-plusMinusTheta, plusMinusTheta);
            // add rotated vector
            curCoords.add(desiredDirectionVector.rotate(theta));
            electronPath[i] = curCoords.copy();
        }

        if (numDaughterBranches > 0) {
            // pick locations for daughterBranches and initialise them:
            for (int i = 0; i < numDaughterBranches, i++) {
                PVector randomElectron = electronPath[random(0, electronPath.length-1)];
                daughterBranches[i] = new Branch(randomElectron.x, randomElectron.y, )
            }

            // initialise new branches
            for (int i = 0; i < numDaughterBranches)
        }
    }
}