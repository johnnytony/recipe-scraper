"""
Main entry point for the recipe scraper application.
"""
from src.classes import RecipeLinkCollector, RecipeInfoExporter

def main():
    """Main function to run the recipe scraper."""
    collector = RecipeLinkCollector()
    recipes_links = collector.get_all_recipes_links()
    
    print(f"Found {len(recipes_links)} recipe links")
    
    exporter = RecipeInfoExporter(recipes_links)
    exporter.export_recipes_info()


if __name__ == "__main__":
    main()

