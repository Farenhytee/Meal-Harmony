package com.example.test;

import androidx.appcompat.app.AlertDialog;
import androidx.appcompat.app.AppCompatActivity;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import android.content.DialogInterface;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.view.inputmethod.InsertGesture;
import android.widget.ArrayAdapter;
import android.widget.Button;

import com.google.android.material.card.MaterialCardView;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class EnterIngredients extends AppCompatActivity {

    MaterialCardView selectIngredients;
    Button addIngredients;
    ArrayList<Integer> ingredientsInt;
    ArrayList<String> ingredients;
    String[] ingredientList = {"Cabbage", "Onions", "Tomatoes", "Cauliflower", "Bhindi", "Potatoes", "Rajma",
            "Paneer", "Chole", "Baingan", "Shimla Mirch", "Sev", "Carrots", "Beans", "Peas", "Lentils", "Green Chilies",
            "Coriander Leaves", "Fenugreek leaves", "Rava", "Poha", "Besan", "Rice", "Urad Dal", "Spinach", "Lauki",
            "Tinda", "Yogurt", "Pumpkin", "Chickpeas", "Peanuts"};
    boolean[] selectedIngredients = new boolean[ingredientList.length];

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_enter_ingredients);

        selectIngredients = findViewById(R.id.mcv_ingredients);
        addIngredients = findViewById(R.id.but_add_ingredients);

        selectIngredients.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                showIngredientsDialog();
            }
        });

    }

    private void showIngredientsDialog() {

        AlertDialog.Builder builder = new AlertDialog.Builder(EnterIngredients.this);

        builder.setTitle("Select Ingredients");
        builder.setCancelable(false);

        builder.setMultiChoiceItems(ingredientList, selectedIngredients, new DialogInterface.OnMultiChoiceClickListener() {
            @Override
            public void onClick(DialogInterface dialog, int which, boolean isChecked) {
                if (isChecked) {
                    ingredientsInt.add(which);
                } else {
                    ingredientsInt.remove(which);
                }
            }
        }).setPositiveButton("Okay", new DialogInterface.OnClickListener() {
            @Override
            public void onClick(DialogInterface dialog, int which) {
                for (int i = 0; i<ingredientsInt.size(); i++) {
                    ingredients.add(ingredientList[ingredientsInt.get(i)]);

                    String s = "";

                    for (int j = 0; j<ingredients.size(); j++) {
                        s += ingredients.get(j) + " ";
                    }

                    Log.d("Ingredients: ", s);
                }
            }
        }).setNegativeButton("Cancel", new DialogInterface.OnClickListener() {
            @Override
            public void onClick(DialogInterface dialog, int which) {
                dialog.dismiss();
            }
        }).setNeutralButton("Clear", new DialogInterface.OnClickListener() {
            @Override
            public void onClick(DialogInterface dialog, int which) {

                Arrays.fill(selectedIngredients, false);

                ingredients.clear();
                ingredientsInt.clear();
            }
        });



        builder.show();
    }
}