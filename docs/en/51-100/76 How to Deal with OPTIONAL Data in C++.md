# Storing Different Types of Data in a Single Variable Series 1/3

Often, we have a function that returns data. For example, we might be reading a file, but what if the file cannot be read? It might not exist, or the data might not be in the format we expect. We still need to return something from the function. In this specific case, we might return an empty string, but that doesn't make much sense. If the file read is empty, we should have a way to see if the data exists.

This is where `std::optional` comes into play, a new feature in the C++17 standard.

```cpp
#include <fstream>

std::string ReadFileAsString(const std::string& filepath)
{
	std::ifstream stream(filepath);
	if(stream)
	{
		std::string result;
		// Read file
		stream.close();
		return result;
	}
	return std::string();

}

int main()
{
	std::string data = ReadFileAsString("data.txt");
	if(data!="")
	{
		// But this way of checking if the file was successfully opened is not ideal
	}
}
```

What we prefer is a way to know if the data was successfully read:

```cpp
std::string ReadFileAsString(const std::string& filepath,bool& outSuccess) // Parameter to determine if the read was successful
{
	std::ifstream stream(filepath);
	if(stream)
	{
		std::string result;
		// Read file
		stream.close();
		outSuccess = true;   // Assign true if read is successful
		return result;
	}
	outSuccess = false;  // Assign false if read fails
	return std::string();

}

int main()
{
	bool fileOpenSuccessfully;
	std::string data = ReadFileAsString("data.txt",fileOpenSuccessfully);
	if(fileOpenSuccessfully)
	{

	}
}
```

This is obviously better than checking for an empty string, but it's still not ideal.
This is where `std::optional` comes in, which is in the header `<optional>`.

```cpp
#include <fstream>
#include <optional>

std::optional <std::string> ReadFileAsString(const std::string& filepath)
{
	std::ifstream stream(filepath);
	if(stream)
	{
		std::string result;
		// Read file
		stream.close();
		return result;
	}
	return {};

}

int main()
{
	std::optional<std::string> data = ReadFileAsString("data.txt"); // Can use auto
	if(data)// Could write data.has_value(), but since the data object has a bool operator, this is more concise
	{
		std::cout << "file read successfully\n";
	}
	else
	{
		std::cout << "file could not read\n";
	}
	std::cin.get();
}
```

You can create a data.txt document in the same directory as the sln file, write something in it, and then run the code to get a successful read prompt.

![](./storage%20bag/Pasted%20image%2020230731184254.png)

You can also use `value_or` to return a default value if the stored value does not exist:

```cpp
std::string value = data.value_or("Not present");
std::cout << value << "\n";
```

![](./storage%20bag/Pasted%20image%2020230731184234.png)

`std::optional::value_or` is a member function that returns the stored value or a default value passed in if the stored value does not exist. In your example, if `data` has a value (i.e., the file was successfully read), `value_or` returns the contents of the file; otherwise, it returns "Not present".