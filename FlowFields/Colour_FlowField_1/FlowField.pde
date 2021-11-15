public class FlowField {
    PVector[] vectors;
    int rows, cols, res;
    float noiseScale = 0.2;
    float zOff = 0.0;
    int hue;
    int[] hues;

    FlowField(int r) {
        res = r;
        cols = (600 / res) + 1;
        rows = (600 / res) + 1;
        vectors = new PVector[rows * cols];
        hues = new int[rows * cols];
    }

    void update() {
        for (int i = 0; i < rows; i++) {
            for (int j = 0; j < cols; j++) {
                float n = noise(j*noiseScale, i*noiseScale, zOff)*2;
                vectors[j + i * cols] = PVector.fromAngle(n*TWO_PI);
                hues[j + i * cols] = floor(n*300);
            }
        }
        zOff += 0.005;
    }
}