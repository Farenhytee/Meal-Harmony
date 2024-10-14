package com.example.test;

import android.content.Context;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;

import java.util.List;

public class rvAdapter extends RecyclerView.Adapter<rvAdapter.MyViewHolder> {
    Context context;
    List<Ingredients> items;

    // Constructor
    public rvAdapter(Context context, List<Ingredients> items) {
        this.context = context;
        this.items = items;
    }

    // ViewHolder class
    public static class MyViewHolder extends RecyclerView.ViewHolder {
        TextView name;

        public MyViewHolder(@NonNull View itemView) {
            super(itemView);
            name = itemView.findViewById(R.id.rv_layout_item_name);
        }
    }

    @NonNull
    @Override
    public MyViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        // Inflate the layout for the item in the RecyclerView
        View view = LayoutInflater.from(context).inflate(R.layout.rv_item_layout, parent, false);
        return new MyViewHolder(view);
    }

    @Override
    public void onBindViewHolder(@NonNull MyViewHolder holder, int position) {
        // Bind data from the item to the views in the ViewHolder
        Ingredients ingredient = items.get(position);
        holder.name.setText(ingredient.getName());
        // Assuming you have an image resource or URL, set it to the image view
        // holder.image.setImageResource(ingredient.getImageResourceId());
        // OR use Glide/Picasso if you are loading images from the internet
    }

    @Override
    public int getItemCount() {
        return items.size(); // Return the size of the list
    }
}
