package com.example.trial

import android.content.Context
import android.graphics.Bitmap
import android.graphics.BitmapFactory
import android.graphics.Matrix
import android.os.Build
import android.os.Bundle
import android.util.Log
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Toast
import androidx.annotation.RequiresApi
import androidx.fragment.app.Fragment
import androidx.navigation.Navigation
import androidx.navigation.fragment.findNavController
import com.android.volley.Response
import com.android.volley.toolbox.Volley
import com.example.trial.databinding.FragmentSecondBinding
import kotlinx.android.synthetic.main.fragment_second.*
import org.json.JSONArray
import org.json.JSONObject
import java.io.ByteArrayOutputStream
import java.io.File
import java.nio.file.Files
import java.nio.file.Path
import java.nio.file.Paths
import java.nio.file.StandardCopyOption


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

    private var responseData: Array<JSONObject?> = Array(4) { null }
    private var responseCount: Int = 0
    private var failureCount: Int = 0
    private var ip: Array<String> = Array(4) { "" }

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
        ip[0] = requireArguments().getString("ip0").orEmpty()
        ip[1] = requireArguments().getString("ip1").orEmpty()
        ip[2] = requireArguments().getString("ip2").orEmpty()
        ip[3] = requireArguments().getString("ip3").orEmpty()

        val bitmap = BitmapFactory.decodeFile(File(imgPath).toString())

        var matrix = Matrix()
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

//        val categories = resources.getStringArray(R.array.Categories)
//        val adapter = ArrayAdapter<String>(requireActivity(),
//            android.R.layout.simple_spinner_item, categories)
//        category_spinner.adapter = adapter
        val default_category = "Car"

        binding.buttonSecond.setOnClickListener {
            val args = requireArguments()
            Navigation.findNavController(requireView()).navigate(R.id.action_SecondFragment_to_FirstFragment, args)
            File(imgPath).delete()
        }

        binding.buttonUpload.setOnClickListener {
            val bitmap_tl = Bitmap.createBitmap(rotatedBitmap, 0, 0, rotatedBitmap.width/2, rotatedBitmap.height/2, null,true)
            sendImage(0, default_category, imgPath, bitmap_tl)  //TL
            val bitmap_tr = Bitmap.createBitmap(rotatedBitmap, rotatedBitmap.width/2, 0, rotatedBitmap.width/2, rotatedBitmap.height/2, null,true)
            sendImage(1, default_category, imgPath, bitmap_tr)  //TR
            val bitmap_bl = Bitmap.createBitmap(rotatedBitmap, 0, rotatedBitmap.height/2, rotatedBitmap.width/2, rotatedBitmap.height/2, null,true)
            sendImage(2, default_category, imgPath, bitmap_bl)  //BL
            val bitmap_br = Bitmap.createBitmap(rotatedBitmap, rotatedBitmap.width/2, rotatedBitmap.height/2, rotatedBitmap.width/2, bitmap.height/2, null,true)
            sendImage(3, default_category, imgPath, bitmap_br)  //BR
        }
    }

    fun sendImage(pos: Int, cat: String, imgPath: String?, rotatedBitmap: Bitmap){
        val stream = ByteArrayOutputStream()
        rotatedBitmap.compress(Bitmap.CompressFormat.PNG, 100, stream)
        val image = stream.toByteArray()
        val filename = imgPath?.split("/")?.get(imgPath?.split("/")!!.size-1)

        if (imgPath != null) {
            sendImage(pos, cat, filename.toString(), image, imgPath)
        }
    }

    fun sendImage(pos: Int, cat: String, filename: String, image: ByteArray, imgPath: String){
        imageData = image
        val queue = Volley.newRequestQueue(thisContext)
//        val url = "http://192.168.0.141:8080/upload"
        val request = @RequiresApi(Build.VERSION_CODES.O)
        object : VolleyFileUploadRequest(
            Method.POST,
            ip[pos],
            Response.Listener {

                responseData[pos] = JSONObject(String(it.data))
                responseCount += 1
                println("Label : ${responseData[pos]?.get("predict_label")}")

                Log.d("TRIAL_APP_REQUEST", it.toString())
                if (responseCount >= 4)
                {
                    var result: Int = 0
                    Toast.makeText(thisContext, "Uploaded succesfully", Toast.LENGTH_SHORT).show()

                    result = calculateResult(responseData)

                    var dataDir = context?.let { getDataDir(it) }

                    if (dataDir != null)
                    {
                        var imgDir = "$dataDir/$result"
                        Files.createDirectories(Paths.get(imgDir))
                        Files.copy(Paths.get(imgPath), Paths.get("$imgDir/$filename"), StandardCopyOption.REPLACE_EXISTING)
                    }


                    val args = requireArguments()
                    args.putString("result", result.toString())
                    findNavController().navigate(R.id.action_SecondFragment_to_ThirdFragment, args)
                }
            },
            Response.ErrorListener {
                failureCount += 1

                Toast.makeText(thisContext, "Oops, something went wrong!", Toast.LENGTH_SHORT).show()
                Log.d("TRIAL_APP_REQUEST", it.toString())

                val args = requireArguments()
                args.putString("result", "Error")
                findNavController().navigate(R.id.action_SecondFragment_to_ThirdFragment, args)
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

    @RequiresApi(Build.VERSION_CODES.O)
    fun calculateResult(responseData: Array<JSONObject?>): Int {

        val cVal = Array(4) { DoubleArray(10) }
        for (i in 0..3) {
            var cArr: JSONArray = responseData[0]?.get("confidence") as JSONArray
            for (j in 0..9) {
                cVal[i][j] = cArr.get(j) as Double
            }
        }
        val sVal = DoubleArray(10)
        var result = -1
        var maxSum: Double = 0.0
        for (i in 0..9) {
            sVal[i] = cVal[0][i] + cVal[1][i] + cVal[2][i] + cVal[3][i]
            if (sVal[i] > maxSum)
            {
                maxSum = sVal[i]
                result = i
            }
        }

        return result
    }

    fun getDataDir(context: Context): String? {
        return context.packageManager
            .getPackageInfo(context.packageName, 0).applicationInfo.dataDir
    }

    override fun onDestroyView() {
        super.onDestroyView()
        _binding = null
    }
}