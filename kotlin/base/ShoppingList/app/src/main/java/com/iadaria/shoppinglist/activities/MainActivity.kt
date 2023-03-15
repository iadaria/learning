package com.iadaria.shoppinglist.activities

import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.util.Log
import com.iadaria.shoppinglist.R
import com.iadaria.shoppinglist.databinding.ActivityMainBinding
import com.iadaria.shoppinglist.fragments.FragmentManager
import com.iadaria.shoppinglist.fragments.NoteFragment

class MainActivity : AppCompatActivity() {
    private lateinit var binding: ActivityMainBinding

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityMainBinding.inflate(layoutInflater)
        setContentView(binding.root)
        setBottomNavListener()
    }

    // слушатель нажатия
    private fun setBottomNavListener() {
        binding.bNavigator.setOnItemSelectedListener {
            when(it.itemId) {
                R.id.settings -> {
                    Log.d("MyLog", "Settings")
                }
                R.id.notes -> {
                    FragmentManager.setFragment(NoteFragment.newInstance(), this)
                }
                R.id.shop_list -> {
                    Log.d("MyLog", "shop_list")
                }
                R.id.new_item -> {
                    FragmentManager.currentFrag?.onClickNew()
                }
            }
            true
        }
    }
}