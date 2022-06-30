"""
Created on Sat Jun 18 11:14:32 2022

@author: ellie
"""

from asyncio.locks import _ContextManagerMixin
from datetime import date
from enum import Enum

class Foodtype(Enum):
    MEAT = 1
    VEGETABLE = 2
    FRUIT = 3
    DRINK = 4
    BAKERY = 5
    RICE = 6
    CEREAL =7

class Item():
    def __init__(self,foodname:str,foodtype:Foodtype,weight:int,expirationdate:date) -> None:
        self.foodname = foodname
        self.foodtype = foodtype
        self.weight = weight
        self.expirationdate = expirationdate

class Ingredient():
    def __init__(self, Ingredient:str,Ingredienttype:Foodtype,Ingredientweight:int) -> None:
        self.ingrename = Ingredient
        self.ingretype = Ingredienttype
        self.ingreweight = Ingredientweight
    
class Recipe():
    def __init__(self,Recipename:str, Ingredients: list[Ingredient]) -> None:
        self.recipename = Recipename
        self.ingredients = Ingredients

class Fridge():
    def __init__(self) -> None:
        self.items = []
    
    def addItem(self,item:Item):
        # self.items.append([item.foodname,item.foodtype,item.weight,item.expirationdate])
        self.items.append(item)
    
    def getAllItems(self):
        print("\n")
        print("We have following items in fridge now:")
        for i,item in enumerate(self.items):
            print(i+1,item.foodname,item.foodtype,item.weight,item.expirationdate)
        print("\n")
    
    def getExpiredItems(self):
        self.expireditems = [] #[item list: Item]
        self.expirednames = [] #[name list: str]
        for item in self.items:
            if item.expirationdate<date.today():
                self.expireditems.append(item)
                self.expirednames.append(item.foodname)
        
        print("This(These) item(s) in fridge is(are) expired: ", set(self.expirednames))
        print("\n")
    
    def remaindExpiring(self):
        self.expiringitems = [] #[item list: Item]
        self.expiringnames = [] #[name list: str]
        for item in self.items:
            if 0<=(item.expirationdate-date.today()).days<=3:
                self.expiringitems.append(item)
                self.expiringnames.append(item.foodname)
        
        print("This(These) item(s) in fridge is(are) will expire in 3 days: ", set(self.expiringnames))
        print("\n")
    
    def clearExpiredItems(self):
        print("We will clean up the expired foods in fridge.")
        self.getExpiredItems()
        for i in self.expireditems:
            self.items.remove(i)
                  
        print("You have removed expired food(s) in our fridge, all items in fridge are fresh now!")
        for i,item in enumerate(self.items):
            print(i+1,":",item.foodname,item.foodtype,item.weight,item.expirationdate)
   
    def cookAndUpdateItem(self,cookrecipe:Recipe,itemlist:list[Item]):
        print("We will use these ingredients today for recipe '%s':" %cookrecipe.recipename.upper())
        ingredientlist = []
        for i in range(len(cookrecipe.ingredients)):
            ingredientlist.append([cookrecipe.ingredients[i].ingrename,cookrecipe.ingredients[i].ingretype,cookrecipe.ingredients[i].ingreweight])
        print(ingredientlist)

        itemlist = sorted(itemlist, key = lambda x: (x.foodname,x.expirationdate,x.weight))
        # sorted ingredients we need in expirationdate/weight

        print("\n")
        print("Before cook, you have these ingredients in fridge:")
        for i,item in enumerate(self.items):
            print(i+1,":",item.foodname,item.foodtype,item.weight,item.expirationdate)

        for i in itemlist:
            for item in self.items:
                for ingret in ingredientlist:
                    if i == item and item.foodname == ingret[0]:
                        if item.weight == ingret[2]:
                            ingret[2] = 0
                            self.items.remove(item)

                        elif item.weight < ingret[2]:
                            ingret[2] -= item.weight
                            if ingret[2] >= 0:
                                self.items.remove(item)
                            else:
                                item.weight =-1*ingret[2]
                                ingret[2] = 0

                        else:
                            item.weight -= ingret[2]
                            ingret[2] = 0

        print("------------------------")
        print("After cooking, you have these ingredients in fridege:")
        for i,item in enumerate(self.items):
            print(i+1,":",item.foodname,item.foodtype,item.weight,item.expirationdate)
        print("\n")


class Menu():
    def __init__(self, fridge) -> None:
        self.fridge = fridge
        self.recipes = []
    
    def addMenu(self,recipe:Recipe):
        self.recipes.append(recipe)

    def displayMenu(self):    
        print("Recipes in our Menu")
        for recipe in self.recipes:
            print(recipe.recipename.upper()," needs ingredients:")
            for num,i in enumerate(range(len(recipe.ingredients))):
                print(num+1,recipe.ingredients[i].ingrename,recipe.ingredients[i].ingretype,recipe.ingredients[i].ingreweight)
            print("\n")
   
    def cookTodayPool(self):
        self.cancooktoday = []
        self.cancooktodaylist = []
        self.enoughingret = []
        self.totalweight = {}

        for recipe in self.recipes:
            for i in range(len(recipe.ingredients)):
                for item in self.fridge.items:
                    if item.foodname == recipe.ingredients[i].ingrename and item.foodtype == recipe.ingredients[i].ingretype and item.expirationdate >= date.today():
                        if item.foodname not in self.totalweight:
                            self.totalweight[item.foodname] = item.weight
                        else:
                            self.totalweight[item.foodname] += item.weight
                        if self.totalweight[item.foodname] >= recipe.ingredients[i].ingreweight:
                            self.enoughingret.append(recipe.ingredients[i].ingrename)
    
        # print("enoughingredients",self.enoughingret)
        
        else:
            for recipe in self.recipes:
                sign = True
                for i in range(len(recipe.ingredients)):
                    if recipe.ingredients[i].ingrename not in self.enoughingret:
                        sign = False
                if sign == True:
                    self.cancooktoday.append(recipe) 
                    self.cancooktodaylist.append(recipe.recipename)        
            # print("cancooktoday",self.cancooktoday)
            if self.cancooktoday == []:
                print("Sorry, you don't have enough fresh ingredients. You can not cook any recipe in our menu today.")
                print("\n")
            else:
                print("We have enough ingredients to cook:",self.cancooktodaylist)
                print("\n")
    
    def cookTodayRecommend(self):
        self.recommend = []
        dic = {}
        countexpirationdays = 36500
        self.cookrecipe = None
        self.itemlist = []
    
        for deal in self.cancooktoday:
            for i in range(len(deal.ingredients)):
                for item in self.fridge.items:
                    if item.foodname == deal.ingredients[i].ingrename and item.foodtype == deal.ingredients[i].ingretype and item.expirationdate >= date.today():
                        if item.foodname not in self.totalweight:
                            self.totalweight[item.foodname] = item.weight
                        else:
                            self.totalweight[item.foodname] += item.weight
                        if self.totalweight[item.foodname] >= deal.ingredients[i].ingreweight:
                            self.itemlist.append(item)
                            if (item.expirationdate-date.today()).days not in dic:
                                dic[(item.expirationdate-date.today()).days]=[[deal.recipename]]
                            elif [deal.recipename] not in dic[(item.expirationdate-date.today()).days]:
                                dic[(item.expirationdate-date.today()).days].append([deal.recipename])
                            countexpirationdays = min(((item.expirationdate-date.today()).days),countexpirationdays)

        if countexpirationdays==36500:
            print("Sorry, some ingredients in fridge are expired. You can not cook any recipe in our menu without refill.")
            print("\n")
            # print("self.cookrecipe",self.cookrecipe, "self.itemlist", self.itemlist)
            return None

        else:
            while True:
                self.recommend = dic[countexpirationdays]
                expiringsoon = []
                for item in self.fridge.items:
                    if (item.expirationdate-date.today()).days == countexpirationdays and item.foodname not in expiringsoon:
                        expiringsoon.append(item.foodname)

                if len(self.recommend) == 1:
                    print("Based on expiration days, you should cook this meal today:",self.recommend[0])
                    print("Ingredient(s) %s will be expired on %s day(s)" % (expiringsoon,countexpirationdays))
                    name = self.recommend[0][0]
                else:
                    print("Based on expiration days, you can cook these meals today: %s. Please choose one!" % self.recommend)
                    print("Ingredient(s) %s will be expired on %s day(s)" % (expiringsoon,countexpirationdays))
                    name = input("Please type the recipe you will cook today:")
                
                if name == 'Q':
                    break

                for recipe in self.recipes:
                    if recipe.recipename == name:
                        self.cookrecipe = recipe
                        break
                if self.cookrecipe == None:
                    print("You may type wrong the recipe name! Please retry! Or type 'Q' to quit.")
                    print("\n")
                else:
                    print("\n")
                    break
                    # return self.cookrecipe, self.itemlist

    
    def chooseRecipe(self):
        while True:
            print("Which recipe you want to cook today? The followings are all recipes in our menu:")
            displaylists = []
            for recipe in self.recipes:
                displaylists.append(recipe.recipename)
            print(displaylists)
            # self.cookTodayPool()

            self.chooserecipename = input("You can type any recipe which you want to cook today.\nIf you don't have enough ingredient(s), we will list the missing or expired ingredient(s) for you:")
            print("\n")
            
            if self.chooserecipename == 'Q':
                break

            self.findingredientlist = []
            for recipe in self.recipes:
                if recipe.recipename == self.chooserecipename:
                    for i in range(len(recipe.ingredients)):
                        self.findingredientlist.append(recipe.ingredients[i])
            if self.findingredientlist ==[]:
                print("Sorry, we don't have %s recipe in our menu. Please retry! Or type 'Q' to quit." % self.chooserecipename.upper())
                print("\n")
            else:
                break

        if self.chooserecipename == 'Q':
            return 
        
        self.cookTodayPool()
        if self.chooserecipename in self.cancooktodaylist:
            print("Yes! You have enough ingredient(s) in fridge to cook %s." % self.chooserecipename.upper())
        else:
            ingredientmissing = []
            ingredientexpiring = []
            ingredientnotenough = [] 
            ingredientcanuse =[]
            self.shoppinglist:Ingredient = [] 
            
            totalweight = {}
            for ingret in self.findingredientlist:
                for item in self.fridge.items:
                    if item.foodname == ingret.ingrename and item.foodtype == ingret.ingretype:
                        if item.expirationdate >= date.today():
                            if item.foodname not in totalweight:
                                totalweight[item.foodname] = item.weight
                            else:
                                totalweight[item.foodname] += item.weight
                            if totalweight[item.foodname] >= ingret.ingreweight and item.foodname not in ingredientcanuse:
                                ingredientcanuse.append(ingret.ingrename)

                            elif 0 <= totalweight[item.foodname] <ingret.ingreweight:
                                ingredientnotenough.append(ingret.ingrename)
                                self.shoppinglist.append(Ingredient(ingret.ingrename,ingret.ingretype,ingret.ingreweight-totalweight[item.foodname]))

                        else:  # item.expirationdate<date.today()
                            if item.foodname not in (ingredientexpiring or ingredientcanuse or ingredientnotenough):
                                ingredientexpiring.append(ingret.ingrename)
                                self.shoppinglist.append(ingret)        
                if ingret.ingrename not in (ingredientmissing or ingredientexpiring or ingredientcanuse or ingredientnotenough):
                    ingredientmissing.append(ingret.ingrename)
                    self.shoppinglist.append(ingret)
  

            if ingredientexpiring or ingredientmissing or ingredientnotenough:
                print("You don't have enough ingredients to cook %s. " % self.chooserecipename.upper())
                if ingredientexpiring:
                    print("ingredient(s) %s in fridge is(are) expired." % ingredientexpiring)
                if ingredientmissing:
                    print("ingredient(s) %s is(are) missing." % ingredientmissing)
                if ingredientnotenough:
                    print("ingredient(s) %s is(are) not enough." % ingredientnotenough)
                print("\n")
                print("You need refill your fridge with following fresh ingredient(s):")
                for i,ingre in enumerate(self.shoppinglist):
                    print(i+1,ingre.ingrename,ingre.ingretype,ingre.ingreweight)

            else:
                print("Yes! You can cook %s today, you have enough ingredients to cook." % self.chooserecipename)
            print("\n")
                
    
 
# start testing

myfridge = Fridge()

# while True:
#     foodname = input("Please input food's name:")
#     foodtype = input("Please input food's type(MEAT,VEGETABLE,FRUIT,DRINK,BAKERY,RICE,CEREAL):")
#     weight = input("Please input food's weight(g):")
#     expirationyear,expirationmonth,expirationday = input("Please input food's expiration Year,Month,Day seperated by space:").split()
#     exdate = date(int(expirationyear),int(expirationmonth),int(expirationday))
#     shoptoday = Item(foodname,foodtype,weight,exdate)
#     myfridge.addItem(shoptoday)
    
#     nextitem = input("Please type any(except'Q') to continue input items or type 'Q' to quit.")
#     if nextitem == 'Q':
#         break

# shoptoday1 = Item('milk','DRINK',1000,date(2022,5,19))
# shoptoday2 = Item('egg','MEAT',20,date(2022,6,30))
# shoptoday3 = Item('tomato','VEGETABLE',1000,date(2022,6,30))
# shoptoday4 = Item('beef','MEAT',1000,date(2022,7,3))
# shoptoday5 = Item('sausage','MEAT',1200,date(2022,5,30))
# shoptoday6 = Item('toufu','VEGETABLE', 1100,date(2022,6,30))


# myfridge.addItem(shoptoday1)
# myfridge.addItem(shoptoday2)
# myfridge.addItem(shoptoday3)
# myfridge.addItem(shoptoday4)
# myfridge.addItem(shoptoday5)
# myfridge.addItem(shoptoday6)

filename1 = 'fridgeshoppinglist.txt'
with open(filename1) as file_object:
    for i, line in enumerate(file_object):
        if i>0:
            item = line.rstrip().split(",")
            shopitem = Item(item[0],item[1],int(item[2]),date(int(item[3]),int(item[4]),int(item[5])))
            myfridge.addItem(shopitem)

myfridge.getAllItems()
myfridge.getExpiredItems()


# pass fridge into Menu object
mymenu = Menu(myfridge)

filename2 = 'menurecipes.txt'
with open(filename2) as file_object:
    for i, line in enumerate(file_object):
        if i>0:
            item = line.rstrip().split(",")
            ingredlist = []
            for i in range((len(item)-1)//3):
                ingredlist.append(Ingredient(item[i*3+1],item[i*3+2],int(item[i*3+3])))
            recipe = Recipe(item[0],ingredlist)
            mymenu.addMenu(recipe)

# egg50 = Ingredient('egg','MEAT',50)
# tomato500 = Ingredient('tomato','VEGETABLE',500)
# beef200 = Ingredient('beef','MEAT',200)
# toufu1000 = Ingredient('toufu','VEGETABLE',1000)
# sausage100 = Ingredient('sausage', 'MEAT', 100)
# mushroom100 = Ingredient('mushroom', 'VEGETABLE', 100)

# eggTomatoRecipe = Recipe("eggtomato", [egg50, tomato500])
# mapoToufuRecipe = Recipe("mapotoufu",[beef200,toufu1000])
# eggSausageRecipe = Recipe("eggsausage", [egg50, sausage100,mushroom100])

# mymenu.addMenu(eggTomatoRecipe)
# mymenu.addMenu(mapoToufuRecipe)
# mymenu.addMenu(eggSausageRecipe)

mymenu.displayMenu()
mymenu.cookTodayPool()
mymenu.cookTodayRecommend()
if mymenu.cookrecipe and mymenu.itemlist:
    cookrecipe,itemlist = mymenu.cookrecipe, mymenu.itemlist
    myfridge.cookAndUpdateItem(cookrecipe,itemlist)

# myfridge.clearExpiredItems()

mymenu.chooseRecipe()
myfridge.remaindExpiring()
