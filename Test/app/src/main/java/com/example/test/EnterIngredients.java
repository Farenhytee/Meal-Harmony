package com.example.test;

import androidx.appcompat.app.AppCompatActivity;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import android.os.Bundle;
import android.view.inputmethod.InsertGesture;
import android.widget.ArrayAdapter;

import java.util.List;

public class EnterIngredients extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_enter_ingredients);

        List<Ingredients> ingredientsList = ch.getServices(need, city);

        RecyclerView available = findViewById(R.id.rv_ingreList);
        ArrayAdapter test = new ArrayAdapter(this, R.layout.rv_item_layout, ingredientsList);
        available.setLayoutManager(new LinearLayoutManager(this));
        available.setAdapter(test);
    }
}