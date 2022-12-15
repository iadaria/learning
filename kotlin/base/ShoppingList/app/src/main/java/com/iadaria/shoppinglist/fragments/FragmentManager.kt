package com.iadaria.shoppinglist.fragments

import androidx.appcompat.app.AppCompatActivity
import com.iadaria.shoppinglist.R

object FragmentManager {
    var currentFrag: BaseFragment? = null

    // переключаемся между фрагментами
    fun setFragment(newFrag: BaseFragment, activity: AppCompatActivity) {
        // С помощью transaction можем удалять/добавлять/менять
        val transaction = activity.supportFragmentManager.beginTransaction()
        // нужно кудата-то помещать
        transaction.replace(R.id.placeHolder, newFrag) // место куда поместим - разметка placeHolder - FrameLoyout
        transaction.commit() // примеянем все действия
        currentFrag = newFrag
    }
}