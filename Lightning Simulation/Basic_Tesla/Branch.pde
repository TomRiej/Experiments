class Branch {
    PVector startCoords;
    int numElectrons = 250;
    PVector[] electronPath = new PVector[numElectrons];
    float theta;
    float plusMinusTheta = PI/16;
 
    Branch(int x, int y) {
        startCoords = new PVector(x, y);
    }

    void saveArc() {
        PVector prevCoords = startCoords.copy();
        // desired arc direction
        PVector desiredDirectionVector = PVector.random2D();

        // save all the electrons
        for (int i = 0; i < numElectrons; i++) {
            // random angle +- theta
            theta = random(-plusMinusTheta, plusMinusTheta);
            // rotated vector
            PVector rotVect = desiredDirectionVector.rotate(theta);
            prevCoords.add(rotVect);
            electronPath[i] = prevCoords.copy();
        }

    }

    void displayArc() {
        noStroke();
        float furthestDist = startCoords.dist(electronPath[electronPath.length-1]);
        for (PVector e : electronPath) {
            // draw the points:
            fill(random(190,240), random(70,100), 100);  // BLUE
            // fill(random(260,270), random(70,100), 100);  // PURPLE
            // fill(random(345,359), random(70,100), 100);  // RED
            // fill(100, random(70, 100), random(40, 80));  // GREEN
            // fill(42, 84, 100);   // GOLD
            float normalDist = (startCoords.dist(e)/furthestDist);
            float radius = lerp(5, 1, (startCoords.dist(e)/furthestDist));
            ellipse(e.x, e.y, radius, radius);
        }
        for (PVector e : electronPath) {
            // draw the points:
            fill(0, 0, 100);
            float radius = lerp(2, 0, (startCoords.dist(e)/furthestDist));
            ellipse(e.x, e.y, radius, radius);
        }
        // noLoop();
    } 
}
