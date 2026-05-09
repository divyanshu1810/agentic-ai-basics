import math

class Circle:
    def __init__(self, radius):
        if radius < 0:
            raise ValueError("Radius can't be negative.")
        self.radius = radius

    def area(self):
        return math.pi * self.radius * self.radius
    
    def perimeter(self):
        return 2 * math.pi * self.radius

def main():
    r = float(input("Enter the radius of the circle: "))
    c = Circle(r)
    print("Area of the circle: ", c.area())
    print("Perimeter of the circle: ", c.perimeter())

if __name__ == "__main__":
    main()
