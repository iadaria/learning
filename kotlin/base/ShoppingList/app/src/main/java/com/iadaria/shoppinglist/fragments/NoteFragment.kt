package com.iadaria.shoppinglist.fragments

import android.app.Activity
import android.content.Intent
import android.os.Bundle
import android.util.Log
import androidx.fragment.app.Fragment
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.activity.result.ActivityResultLauncher
import androidx.activity.result.contract.ActivityResultContracts
import androidx.fragment.app.activityViewModels
import androidx.recyclerview.widget.LinearLayoutManager
import com.iadaria.shoppinglist.R
import com.iadaria.shoppinglist.activities.MainApp
import com.iadaria.shoppinglist.activities.NewNoteActivity
import com.iadaria.shoppinglist.databinding.FragmentNoteBinding
import com.iadaria.shoppinglist.db.MainViewModel
import com.iadaria.shoppinglist.db.NoteAdapter
import com.iadaria.shoppinglist.entities.NoteItem

class NoteFragment : BaseFragment(), NoteAdapter.Listener {
    private lateinit var binding: FragmentNoteBinding
    private lateinit var editLauncher: ActivityResultLauncher<Intent>
    private lateinit var adapter: NoteAdapter

    private val mainViewModel: MainViewModel by activityViewModels {
        MainViewModel.MainViewModelFactory((context?.applicationContext as MainApp).database)
    }

    override fun onClickNew() {
        editLauncher.launch(Intent(activity, NewNoteActivity::class.java))
    }
    // Следит за циклом жизни
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        onEditResult()
    }

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View {
        binding = FragmentNoteBinding.inflate(inflater, container, false)
        return binding.root
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        initRcView()
        observer()
    }

    private fun initRcView() = with(binding) {
        // Как будут идти наши заметки - пока по вертикали
        rcViewNote.layoutManager = LinearLayoutManager(activity)
        // из-за banding нужно явно указать иначе передадим binding вместо fragment
        adapter = NoteAdapter(this@NoteFragment)
        rcViewNote.adapter = adapter
    }

    // следим
    private fun observer() {
        // it - обновленный список
        mainViewModel.allNotes.observe(viewLifecycleOwner) {
            adapter.submitList(it)
        }
    }

    private  fun onEditResult() {
        editLauncher = registerForActivityResult(
            ActivityResultContracts.StartActivityForResult()) {
                if (it.resultCode == Activity.RESULT_OK) {
                    val editState = it.data?.getStringExtra(EDIT_STATE_KEY)
                    val newNote: NoteItem = it.data?.getSerializableExtra(NEW_NOTE_KEY) as NoteItem
                    if (editState == "update") {
                        mainViewModel.updateNote(newNote)
                    } else {
                        mainViewModel.insertNote(newNote)
                    }
                }
        }
    }

    override fun deleteItem(id: Int) {
        mainViewModel.deleteNote(id)
    }

    override fun onClickItem(note: NoteItem) {
        val intent = Intent(activity, NewNoteActivity::class.java).apply {
            putExtra(NEW_NOTE_KEY, note)
        }
        editLauncher.launch(intent)
    }

    companion object {
        const val NEW_NOTE_KEY = "new_note_key"
        const val EDIT_STATE_KEY = "edit_state_key"
        @JvmStatic
        fun newInstance() = NoteFragment()
    }
}