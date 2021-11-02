class Branch {
    PVector startCoords;
    int recursionDepth;
    Branch[] daughterBranches;
    int numDaughterBranches;
    int numElectrons;
    PVector[] electronPath;
    PVector[] branchedElectrons;
    float theta;
    float plusMinusTheta = PI/16;

    Branch(int x, int y, int recDepth) {
        startCoords = new PVector(x, y);
        recursionDepth = recDepth;
        switch (recursionDepth) {
            case 0:
                numDaughterBranches = int(random(2, 5));
                numElectrons = 250;
                break;
            case 1:
                numDaughterBranches = int(random(1, 3));
                numElectrons = 50;
                break;
            case 2:
                numDaughterBranches = int(random(0, 1));
                numElectrons = 20;
                break;
            default:
                numDaughterBranches = 0;
        }
        // init electron path array for this branch
        electronPath = new PVector[numElectrons];

        // initialise daughter branch array
        if (numDaughterBranches != 0) {
            daughterBranches = new Branch[numDaughterBranches];
            branchedElectrons = new PVector[numDaughterBranches]; // herer
        }
    }

    void saveArc(PVector desiredDirectionVector) {
        // make the main arc
        PVector curCoords = startCoords.copy();

        for (int i = 0; i < numElectrons; i++) {
            theta = random(-plusMinusTheta, plusMinusTheta);
            // add rotated vector
            curCoords.add(desiredDirectionVector.rotate(theta));
            electronPath[i] = curCoords.copy();
        }

        // for each branch: (zero will result in this loop never running)
        for (int i = 0; i < numDaughterBranches; i++) {
            // pick random starting electron
            PVector randomElectron = electronPath[int(random(0, electronPath.length-1))];
            // Initialise new branch off this electron
            daughterBranches[i] = new Branch(int(randomElectron.x), int(randomElectron.y), recursionDepth+1);
            // save the arc for this branch
            daughterBranches[i].saveArc(desiredDirectionVector.rotate(theta));
        }
    }

    float calcFurthestDist() {
        return startCoords.dist(electronPath[electronPath.length-1]);
    }

    void drawArcGlow(float startRadius) {
        noStroke();
        // draw the blue for the branches
        if (numDaughterBranches > 0) {
            for (Branch branch : daughterBranches) {
                branch.drawArcGlow(startRadius);
            }
        }


        for (int i = 0; i < numElectrons; i++) {
            PVector e = electronPath[i];
            // random blue colour
            fill(random(190,240), random(70,100), 100);
            // find the radius of the ellipse
            float radius = lerp(startRadius, 1, float(i)/float(numElectrons));

            ellipse(e.x, e.y, radius, radius);
        }
    }

    void drawArcMain() {
        noStroke();
        // First the blue glow for all
        fill(random(190,240), random(70,100), 100);
        // draw each of the branches first
        // if (numDaughterBranches > 0) {
        //     for (Branch branch : daughterBranches) {
        //         branch.drawArc();
        //     }
        // }
        
        // draw the main path
        for (PVector e : electronPath) {
            ellipse(e.x, e.y, 2, 2);
        }
    }
}