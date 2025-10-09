import OpenGL.GL as gl
import glfw

def update_visualizer(data):
    gl.glUniform1f(gl.glGetUniformLocation(shader, "entropy"), data["entropy"])
    gl.glUniform1f(gl.glGetUniformLocation(shader, "coherence"), data["coherence"])
