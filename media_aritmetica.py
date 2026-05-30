import pandas as pd

df_est = pd.read_csv("datos_estudiantes.csv")

media_art = df_est['edad'].mean()

print("--- MEDIA ARITMÉTICA ---")
print(f"La edad promedio de los estudiantes es: {media_art:.2f} años")


