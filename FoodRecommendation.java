import java.util.*;
import java.util.stream.Collectors;

public class FoodRecommendation {

    // Dish data for user 35
    static int userId = 35;

    static Map<String, Double> dishesData = new HashMap<String, Double>() {{
        put("Patta Gobi", 2.8);
        put("Phool Gobi", 2.4);
        put("Bhindi", 3.4);
        put("Aloo Sabzi", 3.6);
        put("Rajma", 3.4);
        put("Paneer", 3.8);
        put("Chole", 3.6);
        put("Baingan", 3.2);
        put("Shimla Mirch", 2.9);
        put("Sev Tamatar", 1.8);
        put("Malai Pyaaz", 2.4);
        put("Mix Veg", 2.4);
        put("Any Dal", 3.6);
        put("Aloo Paratha", 3.4);
        put("Pyaaz Paratha", 3.6);
        put("Paneer Paratha", 2.4);
    }};

    static List<String> dishNames = new ArrayList<>(dishesData.keySet());

    static Map<Integer, List<Double>> dishes = new HashMap<Integer, List<Double>>() {{
        put(userId, new ArrayList<>(dishesData.values()));
    }};
    
    static double[][] dishSimilarity = cosineSimilarity(dishes.get(userId));

    // Store recently selected dishes
    static Map<Integer, List<Integer>> recentlySelected = new HashMap<>();

    public static double[][] cosineSimilarity(List<Double> ratings) {
        int size = ratings.size();
        double[][] similarityMatrix = new double[size][size];

        for (int i = 0; i < size; i++) {
            for (int j = i; j < size; j++) {
                double dotProduct = ratings.get(i) * ratings.get(j);
                double normA = Math.sqrt(ratings.get(i) * ratings.get(i));
                double normB = Math.sqrt(ratings.get(j) * ratings.get(j));
                double similarity = dotProduct / (normA * normB);

                similarityMatrix[i][j] = similarity;
                similarityMatrix[j][i] = similarity;  // Symmetric matrix
            }
        }

        return similarityMatrix;
    }

    public static List<Integer> selectNeighborhood(double[][] similarityMatrix, int itemId, int neighborhoodSize) {
        double[] itemSimilarityScores = similarityMatrix[itemId];
        List<Integer> sortedIndices = new ArrayList<>();

        for (int i = 0; i < itemSimilarityScores.length; i++) {
            sortedIndices.add(i);
        }

        sortedIndices.sort((a, b) -> Double.compare(itemSimilarityScores[b], itemSimilarityScores[a]));
        return sortedIndices.subList(1, neighborhoodSize + 1);  // Exclude the item itself
    }

    public static void updateData(int userId, int selectedDish, int neighborhoodSize) {
        List<Integer> neighborhood = selectNeighborhood(dishSimilarity, selectedDish, neighborhoodSize);

        for (int i : neighborhood) {
            double currentRating = dishes.get(userId).get(i);
            double adjustment = dishSimilarity[selectedDish][i] < 0.5 ? 0.1 : (currentRating > 1.2 ? -0.2 : 0);
            dishSimilarity[selectedDish][i] += adjustment;

            double newRating = Math.min(Math.max(dishes.get(userId).get(i) + adjustment, 1), 5);
            dishes.get(userId).set(i, (double) Math.round(newRating * 10) / 10);
        }

        recentlySelected.computeIfAbsent(userId, k -> new ArrayList<>());
        recentlySelected.get(userId).add(selectedDish);

        if (recentlySelected.get(userId).size() > 3) {
            recentlySelected.get(userId).remove(0);  // Maintain recent selections
        }
    }

    public static List<String> getRecommendations(int userId, int numRecommendations) {
        List<Double> userRatings = dishes.get(userId);
        List<Integer> unratedDishes = new ArrayList<>();

        for (int i = 0; i < userRatings.size(); i++) {
            if (userRatings.get(i) < 3) {
                unratedDishes.add(i);
            }
        }

        List<Integer> sortedUnrated = unratedDishes.stream().sorted(Comparator.comparing(userRatings::get).reversed()).collect(Collectors.toList());

        List<Integer> finalRecommendations = sortedUnrated.stream().filter(i -> !recentlySelected.getOrDefault(userId, new ArrayList<>()).contains(i))
                .limit(numRecommendations)
                .collect(Collectors.toList());

        return finalRecommendations.stream()
                .map(i -> dishNames.get(i))
                .collect(Collectors.toList());
    }

    public static List<String> getRecs() {
        return getRecommendations(35, 5);
    }

    public static void main(String[] args) {
        // Example usage
        System.out.println(getRecs());
    }
}
