package com.example.test;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;

import java.util.ArrayList;
import java.util.List;

public class GetRecommendations extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_get_recommendations);

        FoodRecommendation fr = new FoodRecommendation();

        List<String> recoms = fr.getRecs();

        Button setRecs = findViewById(R.id.but_Get);
        TextView d1 = findViewById(R.id.tv_dish1);
        TextView d2 = findViewById(R.id.tv_dish2);
        TextView d3 = findViewById(R.id.tv_dish3);
        TextView d4 = findViewById(R.id.tv_dish4);
        TextView d5 = findViewById(R.id.tv_dish5);

        setRecs.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                d1.setText(recoms.get(0));
                d2.setText(recoms.get(1));
                d3.setText(recoms.get(2));
                d4.setText(recoms.get(3));
                d5.setText(recoms.get(4));
            }
        });

    }
}