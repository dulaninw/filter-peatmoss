import os
import json
import pandas as pd

files_to_check = [f for f in os.listdir("final_analysis/") if ".json" in f]

total_data_points = 0
total_additions = 0
total_updates = 0
total_removals = 0

total_integration_patterns = 0
total_task_specifity = 0
total_comm_and_collab = 0
total_maintenance = 0
total_compliance = 0
total_perform_improvements = 0
total_compatability = 0
total_deprecation = 0
total_project_evol = 0
total_simplification = 0

file_df = pd.DataFrame(columns=['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11'])
for file in files_to_check:
    f = open(f"final_analysis/{file}")
    data = json.load(f)
    
    file_integration_patterns = 0
    file_task_specifity = 0
    file_comm_and_collab = 0
    file_maintenance = 0
    file_compliance = 0
    file_perform_improvements = 0
    file_compatability = 0
    file_deprecation = 0
    file_project_evol = 0
    file_simplification = 0
    
    file_data_points = 0
    for data_point in data:
        file_data_points += 1
        text = data_point["text"]
        for cat in text:
            if 'Integration Patterns' in cat and cat['Integration Patterns'] != None and cat['Integration Patterns'] != "" and cat['Integration Patterns'] != "No" and cat['Integration Patterns'] != "None":
                file_integration_patterns += 1
            if 'Task Specificity' in cat and cat['Task Specificity'] != None and cat['Task Specificity'] != "" and cat['Task Specificity'] != "No" and cat['Task Specificity'] != "None":
                file_task_specifity += 1
            if 'Community and Collaboration' in cat and cat['Community and Collaboration'] != None and cat['Community and Collaboration'] != "" and cat['Community and Collaboration'] != "No" and cat['Community and Collaboration'] != "None":
                file_comm_and_collab += 1
            if 'Maintenance' in cat and cat['Maintenance'] != None and cat['Maintenance'] != "" and cat['Maintenance'] != "No" and cat['Maintenance'] != "None":
                file_maintenance += 1
            if 'Compliance and Standards' in cat and cat['Compliance and Standards'] != None and cat['Compliance and Standards'] != "" and cat['Compliance and Standards'] != "No" and cat['Compliance and Standards'] != "None":
                file_compliance += 1
            if 'Performance Improvements' in cat and cat['Performance Improvements'] != None and cat['Performance Improvements'] != "" and cat['Performance Improvements'] != "No" and cat['Performance Improvements'] != "None":
                file_perform_improvements += 1
            if 'Compatibility' in cat and cat['Compatibility'] != None and cat['Compatibility'] != "" and cat['Compatibility'] != "No" and cat['Compatibility'] != "None":
                file_compatability += 1
            if 'Deprecation and Replacement' in cat and cat['Deprecation and Replacement'] != None and cat['Deprecation and Replacement'] != "" and cat['Deprecation and Replacement'] != "No" and cat['Deprecation and Replacement'] != "None":
                file_deprecation += 1
            if 'Project Evolution' in cat and cat['Project Evolution'] != None and cat['Project Evolution'] != "" and cat['Project Evolution'] != "No" and cat['Project Evolution'] != "None":
                file_project_evol += 1
            if 'Technical Debt and Simplification' in cat and cat['Technical Debt and Simplification'] != None and cat['Technical Debt and Simplification'] != "" and cat['Technical Debt and Simplification'] != "No" and cat['Technical Debt and Simplification'] != "None":
                file_simplification += 1
    
    file_df.loc[len(file_df.index)] = [file, file_data_points, file_integration_patterns, file_task_specifity, file_comm_and_collab, file_maintenance, file_compliance, file_perform_improvements, file_compatability, file_deprecation, file_project_evol, file_simplification]
    
    total_data_points += file_data_points
    total_integration_patterns += file_integration_patterns
    total_task_specifity += file_task_specifity
    total_comm_and_collab += file_comm_and_collab
    total_maintenance += file_maintenance
    total_compliance += file_compliance
    total_perform_improvements += file_perform_improvements
    total_compatability += file_compatability
    total_deprecation += file_deprecation
    total_project_evol += file_project_evol
    total_simplification += file_simplification

file_df.columns = ["File Name", "# of Datapoints", "Integration Patterns", "Task Specificity", "Community and Collaboration", "Maintenance", "Compliance and Standards", "Performance Improvements", "Compatibility", "Deprecation and Replacement", "Project Evolution", "Technical Debt and Simplification"]
file_df.to_csv("file_analysis_category_counts.csv", index=False)


"""
Code to generate a text file with the breakdown of the categories
File contains the total number of datapoints across all 22 json files in the final_analysis folder,
and the number of additions, updates, and removals.
"""
write_file = open("final_analysis_breakdown.txt", "w", encoding="utf-8", errors="ignore")
write_file.write(f"Breakdown of dataset:\n")
write_file.write(f"Number of Datapoints: {total_data_points}\n\n")

total_additions += total_integration_patterns + total_task_specifity + total_comm_and_collab
total_updates += total_maintenance + total_compliance + total_perform_improvements + total_compatability
total_removals += total_deprecation + total_project_evol + total_simplification

write_file.write(f"Total additions: {total_additions}\n")
write_file.write(f"  integration patterns: {total_integration_patterns}\n")
write_file.write(f"  task specificity: {total_task_specifity}\n")
write_file.write(f"  community and collaboration: {total_comm_and_collab}\n\n")

write_file.write(f"Total updates: {total_updates}\n")
write_file.write(f"  maintenance: {total_maintenance}\n")
write_file.write(f"  compliance and standards: {total_compliance}\n")
write_file.write(f"  performance improvements: {total_perform_improvements}\n")
write_file.write(f"  compatibility: {total_compatability}\n\n")

write_file.write(f"Total removals: {total_removals}\n")
write_file.write(f"  deprecation and replacement: {total_deprecation}\n")
write_file.write(f"  project evolution: {total_project_evol}\n")
write_file.write(f"  technical debt and simplification: {total_simplification}\n\n")

    