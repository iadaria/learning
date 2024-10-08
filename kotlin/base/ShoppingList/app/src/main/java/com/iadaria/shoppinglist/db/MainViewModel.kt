package com.iadaria.shoppinglist.db

import androidx.lifecycle.*
import com.iadaria.shoppinglist.entities.NoteItem
import kotlinx.coroutines.launch

class MainViewModel(database: MainDatabase) : ViewModel() {
    val dao = database.getDao()
    val allNotes: LiveData<List<NoteItem>> = dao.getAllNotes().asLiveData()

    fun insertNote(note: NoteItem) = viewModelScope.launch {
        dao.insertNote(note)
    }

    fun updateNote(note: NoteItem) = viewModelScope.launch {
        dao.updateNote(note)
    }
    fun deleteNote(id: Int) = viewModelScope.launch {
        dao.deleteNote(id)
    }

    class MainViewModelFactory(val database: MainDatabase): ViewModelProvider.Factory {
        override fun <T : ViewModel> create(modelClass: Class<T>): T {
            if (modelClass.isAssignableFrom(MainViewModel::class.java)) {
                @Suppress("UNCHECKED_CAST")
                return MainViewModel(database) as T
            }
            throw IllegalArgumentException("Unknown VeiwModalClass")
        }
    }
}