import turtle

# Khởi tạo màn hình turtle
t = turtle.Turtle()
t.speed(0)
t.hideturtle()

# Vẽ cầu vồng
colors = ['red', 'orange', 'yellow', 'green', 'blue', 'indigo', 'violet']
size = 100

for i in range(len(colors)):
    t.pencolor(colors[i])
    t.fillcolor(colors[i])
    t.begin_fill()
    t.circle(size)
    size -= 10
    t.end_fill()

# Hiển thị đồ hoạ
turtle.done()
