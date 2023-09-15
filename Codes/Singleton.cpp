#include <iostream>

class Random
{
public:
	Random(const Random&) = delete;
	static Random& Get()
	{
		static Random s_Instance;
		return  s_Instance;
	}
	static float Float() { return Get().IFloat(); }
private:
	float IFloat() { return m_RandomGenerator; };
	Random() {};
	float m_RandomGenerator = 0.5f;
};

namespace RandomClass  
{
	static float s_RandomGenerator = 0.5f;
	static float Float() { return s_RandomGenerator; }
}

int main()
{
	float number = Random::Float();
	std::cout << number << "\n";
}