import Distribution.SPDX (LicenseId(SugarCRM_1_1_3))
import Distribution.Simple.Utils (xargs)
import Text.XHtml (base)
fatorial :: Int -> Int
fatorial 0 = 1
fatorial x = x * fatorial (x-1)

meuHead :: [Int] -> Int
meuHead [] = error "Lista vazia"
meuHead (x:xs) = x

nomes = ["alice", "bob", "charlie"]
saudações = map (\x -> "Ola, " ++ x) nomes

newtype UserId = UserId Int
data StatusLogin = Deslogado | Logando String | Logado UserId String 
mensagemStatus :: StatusLogin -> String
mensagemStatus Deslogado = "Usuario deslogado"
mensagemStatus (Logando usuario) = "Tentando logar como: " ++ usuario
mensagemStatus (Logado (UserId(id)) usuario) = "Usuario: " ++ usuario ++ " logado com id: " ++ show id

data Nat = Zero | Suc Nat
um :: Nat
um = Suc Zero

dois :: Nat
dois = Suc um

tres :: Nat
tres = Suc dois

quatro :: Nat
quatro = Suc tres

nat2integer :: Nat -> Integer
nat2integer Zero = 0
nat2integer (Suc x) = 1 + nat2integer x

integer2nat :: Integer -> Nat
integer2nat 0 = Zero
integer2nat x = Suc(integer2nat (x-1))

natAdd :: Nat -> Nat -> Nat
natAdd Zero x = x
natAdd (Suc y) x = Suc (natAdd y x)

natSub :: Nat -> Nat -> Nat
natSub x Zero = x
natSub Zero (Suc x) = error "Resultado negativo"
natSub (Suc x) (Suc y) = natSub x y

natMul :: Nat -> Nat -> Nat
natMul Zero x = Zero;
natMul (Suc x) y = natAdd y (natMul x y)

salario :: Double -> Double
salario x = x*1.03

calculaMedia :: Double -> Double -> Double -> String
calculaMedia x y z
 | media >= 8 = "A"
 | media >= 7 = "B"
 | media >= 6 = "C"
 | media >= 5 = "D"
 | otherwise = "E"
 where 
    media = (x*2+y*3+z*5)/10

precoRetrato :: Integer -> String -> Double
precoRetrato num dia
 | dia == "sabado" = base*1.2
 | dia == "domingo" = base*1.2
 | otherwise = base
 where 
    base
        | num == 1 = 100
        | num == 2 = 130
        | num == 3 = 150
        | num == 4 = 165
        | num == 5 = 175
        | num == 6 = 180
        | otherwise = 185

fatorialDuplo :: Int -> Int
fatorialDuplo 1 = 1
fatorialDuplo 2 = 2
fatorialDuplo x = x * fatorialDuplo(x-2)

potencia :: Int -> Int -> Int
potencia x 1 = x
potencia x y = x * (potencia x (y-1))

taxa :: Int -> Double
taxa 1 = 0.015
taxa x = 2 * taxa(x-1)

salarioAnos :: Int -> Double -> Double
salarioAnos 0 base = base
salarioAnos x base = salarioAnos (x-1) base * (1+ taxa x)

salarioAtual :: Double -> Int -> Int -> Double
salarioAtual sal a1 a2 = 
    salarioAnos (a2 - a1) sal

ultimo :: [a] -> a
ultimo [x] = x
ultimo (x:xs) = ultimo (xs)

primeiros :: [a] -> [a]
primeiros [x] = []
primeiros (x:xs) = x : primeiros xs

mulList :: Num a => [a] -> [a] -> [a]
mulList [] [] = []
mulList (x:xs) (y:ys) = x*y : mulList xs ys