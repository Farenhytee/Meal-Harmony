package com.example.test;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;

public class Home extends AppCompatActivity {

    private static final String PREFS_NAME = "user";
    private static final String KEY_USER_ID = "id";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_home);

        Button selectADish = findViewById(R.id.but_EnterSelection);
        Button getRecommendations = findViewById(R.id.but_GetRecommendations);
        Button viewRecent = findViewById(R.id.but_ViewRecent);
        Button enterIngr = findViewById(R.id.but_enterIngredients);

        selectADish.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent = new Intent(Home.this, SelectADish.class);
                startActivity(intent);
            }
        });

        getRecommendations.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent = new Intent(Home.this, GetRecommendations.class);
                startActivity(intent);
            }
        });

        viewRecent.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent = new Intent(Home.this, ViewRecentDishes.class);
                startActivity(intent);
            }
        });

        enterIngr.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent = new Intent(Home.this, EnterIngredients.class);
                startActivity(intent);
            }
        });

    }
}