package com.example.trial

import android.content.Context
import android.os.Bundle
import androidx.fragment.app.Fragment
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.navigation.fragment.findNavController
import com.example.trial.databinding.FragmentThirdBinding
import kotlinx.android.synthetic.main.fragment_third.*
import org.json.JSONObject

/**
 * A simple [Fragment] subclass.
 * Use the [ThirdFragment.newInstance] factory method to
 * create an instance of this fragment.
 */
class ThirdFragment : Fragment() {

    private var _binding: FragmentThirdBinding? = null

    // This property is only valid between onCreateView and
    // onDestroyView.
    private val binding get() = _binding!!

    var thisContext: Context? = null

    private var responseData: Array<JSONObject?> = Array(4) { null }

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        _binding = FragmentThirdBinding.inflate(inflater, container, false)
        thisContext = container?.getContext()
        return binding.root
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        val result = requireArguments().getString("result")
        outputTextView.text = result

        binding.resetButton.setOnClickListener {
            val args = requireArguments()
            findNavController().navigate(R.id.action_ThirdFragment_to_FirstFragment, args)
        }
    }

}