package com.example.trial

import android.content.Context
import android.os.Bundle
import android.os.StrictMode
import android.os.StrictMode.VmPolicy
import android.system.Os.socket
import android.util.Log
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Button
import android.widget.Switch
import android.widget.Toast
import androidx.fragment.app.Fragment
import androidx.lifecycle.lifecycleScope
import androidx.navigation.fragment.findNavController
import com.example.trial.databinding.FragmentSetupBinding
import kotlinx.android.synthetic.main.fragment_setup.*
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import java.io.BufferedReader
import java.io.InputStreamReader
import java.net.*
import java.util.*

/**
 * A simple [Fragment] subclass.
 * Use the [SetupFragment.newInstance] factory method to
 * create an instance of this fragment.
 */
class SetupFragment : Fragment() {

    private var _binding: FragmentSetupBinding? = null

    // This property is only valid between onCreateView and
    // onDestroyView.
    private val binding get() = _binding!!

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {

        _binding = FragmentSetupBinding.inflate(inflater, container, false)
        return binding.root
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)


        binding.setValuesbutton.setOnClickListener {
            val ipPort = ":8080/upload"
            val ipPre = "http://"
            var ip0 = ipPre + tlIPText.text.toString() + ipPort
            var ip1 = ipPre + trIPText.text.toString() + ipPort
            var ip2 = ipPre + blIPText.text.toString() + ipPort
            var ip3 = ipPre + brIPText.text.toString() + ipPort
            val args = Bundle()
            args.putString("ip0", ip0)
            args.putString("ip1", ip1)
            args.putString("ip2", ip2)
            args.putString("ip3", ip3)
            findNavController().navigate(R.id.action_SetupFragment_to_FirstFragment, args)
        }

        binding.setDefaultButton.setOnClickListener {
            val ipDef = "http://192.168.0.141"
            var ipPort = ":8080/upload"
            var ip0 = ipDef + ipPort
            var ip1 = ipDef + ipPort
            var ip2 = ipDef + ipPort
            var ip3 = ipDef + ipPort
            val args = Bundle()
            args.putString("ip0", ip0)
            args.putString("ip1", ip1)
            args.putString("ip2", ip2)
            args.putString("ip3", ip3)
            findNavController().navigate(R.id.action_SetupFragment_to_FirstFragment, args)
        }

    }

}