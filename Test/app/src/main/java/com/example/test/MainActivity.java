package com.example.test;

import androidx.appcompat.app.AppCompatActivity;
import android.content.SharedPreferences;
import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;

public class MainActivity extends AppCompatActivity {

    private static final String PREFS_NAME = "user";
    private static final String KEY_USER_ID = "id";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        Button start = findViewById(R.id.but_Start);
        EditText user_id = findViewById(R.id.et_UserID);

        SharedPreferences sharedPreferences = getSharedPreferences(PREFS_NAME, MODE_PRIVATE);
        SharedPreferences.Editor editor = sharedPreferences.edit();

        start.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {

                Intent intent = new Intent(MainActivity.this, Home.class);
                int id = Integer.parseInt(user_id.getText().toString());

                editor.putInt(KEY_USER_ID, id); // Example: storing user ID as 123
                editor.apply();

                startActivity(intent);
            }
        });

    }
}