package com.example.test;

import android.view.View;
import android.widget.ImageView;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;

public class viewHolder extends RecyclerView.ViewHolder {
    TextView name;
    public viewHolder(@NonNull View itemView) {
        super(itemView);
        name = itemView.findViewById(R.id.rv_layout_item_name);

    }
}