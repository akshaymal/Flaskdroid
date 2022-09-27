package com.example.trial

import android.content.Context
import android.graphics.Bitmap
import android.graphics.BitmapFactory
import android.graphics.Matrix
import android.os.Bundle
import android.util.Log
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.*
import androidx.fragment.app.Fragment
import androidx.navigation.Navigation
import androidx.navigation.fragment.findNavController
import com.android.volley.Response
import com.android.volley.toolbox.Volley
import com.example.trial.databinding.FragmentSecondBinding
import kotlinx.android.synthetic.main.activity_main.*
import kotlinx.android.synthetic.main.fragment_second.*
import java.io.ByteArrayOutputStream
import java.io.File


/**
 * A simple [Fragment] subclass as the second destination in the navigation.
 */
class SecondFragment : Fragment() {

    private var _binding: FragmentSecondBinding? = null

    // This property is only valid between onCreateView and
    // onDestroyView.
    private val binding get() = _binding!!

    var thisContext: Context? = null

    private var imageData: ByteArray? = null

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {

        _binding = FragmentSecondBinding.inflate(inflater, container, false)
        thisContext = container?.getContext()
        return binding.root

    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        val imgPath = requireArguments().getString("CurrImage")
        val bitmap = BitmapFactory.decodeFile(File(imgPath).toString())

        val matrix = Matrix()
        matrix.postRotate(90F)
//        val scaledBitmap = Bitmap.createScaledBitmap(bitmap, width, height, true)

        val rotatedBitmap = Bitmap.createBitmap(
            bitmap,
            0,
            0,
            bitmap.width,
            bitmap.height,
            matrix,
            true
        )
        val stream = ByteArrayOutputStream()


        imageView.setImageBitmap(rotatedBitmap)

        val categories = resources.getStringArray(R.array.Categories)
        val adapter = ArrayAdapter<String>(requireActivity(),
            android.R.layout.simple_spinner_item, categories)
        category_spinner.adapter = adapter

        binding.buttonSecond.setOnClickListener {
            Navigation.findNavController(requireView()).navigate(R.id.action_SecondFragment_to_FirstFragment)
            File(imgPath).delete()
        }

        binding.buttonUpload.setOnClickListener {
            rotatedBitmap.compress(Bitmap.CompressFormat.PNG, 100, stream)
            val image = stream.toByteArray()
            val filename = imgPath?.split("/")?.get(imgPath?.split("/")!!.size-1)

            sendImage(category_spinner.selectedItem.toString(), filename.toString(), image)
        }
    }

    fun sendImage(cat: String, filename: String, image: ByteArray){
        imageData = image
        val queue = Volley.newRequestQueue(thisContext)
        val url = "http://192.168.0.51:5000/upload"
        val request = object : VolleyFileUploadRequest(
            Method.POST,
            url,
            Response.Listener {

                Toast.makeText(thisContext, "Uploaded succesfully", Toast.LENGTH_SHORT).show()
                Log.d("TRIAL_APP_REQUEST", it.toString())
                findNavController().navigate(R.id.action_SecondFragment_to_FirstFragment)

            },
            Response.ErrorListener {
                Toast.makeText(thisContext, "Oops, something went wrong!", Toast.LENGTH_SHORT).show()

                Log.d("TRIAL_APP_REQUEST", it.toString())
            }
        ) {
            override fun getParams(): MutableMap<String, String>? {
                val params = HashMap<String, String>()
                params.put("category", cat)
                return params
            }
            override fun getByteData(): MutableMap<String, FileDataPart> {
                var params = HashMap<String, FileDataPart>()
                params["file"] = FileDataPart(filename, imageData!!, "jpeg")

                return params
            }
        }
        queue.add(request)

    }

    override fun onDestroyView() {
        super.onDestroyView()
        _binding = null
    }
}